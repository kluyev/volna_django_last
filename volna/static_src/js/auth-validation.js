const passwordChangeForm = document.querySelector('form[action*="password-change"]');

if (passwordChangeForm) {
    passwordChangeForm.addEventListener('submit', function(e) {
        const newPassword1 = document.getElementById('id_new_password1');
        const newPassword2 = document.getElementById('id_new_password2');
        
        if (newPassword1 && newPassword2 && newPassword1.value !== newPassword2.value) {
            e.preventDefault();
            showToast('Пароли не совпадают');
            return false;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Элементы формы
    const form = document.querySelector('form');
    const firstNameInput = document.querySelector('[name="first_name"]');
    const usernameInput = document.querySelector('[name="username"]');
    const passwordInput = document.getElementById('password-input');
    const strengthBar = document.getElementById('password-strength');

    // 1. Валидация имени
    firstNameInput.addEventListener('blur', validateName);
    function validateName() {
        const value = this.value.trim();
        clearError(this);
        
        if (value.length < 2) {
            showError(this, 'Имя должно содержать минимум 2 символа');
            return false;
        }
        return true;
    }

    // 2. Валидация логина
    usernameInput.addEventListener('blur', validateUsername);
    async function validateUsername() {
        const username = this.value.trim();
        clearError(this);
        
        if (username.length < 3) {
            showError(this, 'Логин слишком короткий (минимум 3 символа)');
            return false;
        }
        
        try {
            const response = await fetch(`{% url 'check_username' %}?username=${encodeURIComponent(username)}`);
            const data = await response.json();
            
            if (data.exists) {
                showError(this, 'Этот логин уже занят');
                return false;
            }
            return true;
        } catch (error) {
            console.error('Ошибка проверки логина:', error);
            return true; // Пропускаем, если сервер не ответил
        }
    }

    // 3. Валидация пароля (индикатор сложности)
    if (passwordInput && strengthBar) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            const tips = [];
            
            // Критерии проверки
            if (password.length >= 8) strength += 1;
            if (password.length >= 12) strength += 1;
            if (/[A-Z]/.test(password)) strength += 1;
            if (/[0-9]/.test(password)) strength += 1;
            if (/[^A-Za-z0-9]/.test(password)) strength += 1;
            
            // Визуализация
            const strengthText = ['Очень слабая', 'Слабая', 'Средняя', 'Хорошая', 'Отличная'][strength] || 'Недостаточная';
            const colors = ['#ff4d4d', '#ff6b6b', '#feca57', '#48dbfb', '#1dd1a1'];
            
            strengthBar.innerHTML = `
                <div class="progress mt-2" style="height: 5px">
                    <div class="progress-bar" 
                         style="width: ${strength * 20}%; 
                                background: ${colors[strength] || '#ddd'}">
                    </div>
                </div>
                <small class="d-block mt-1">Сложность: <strong>${strengthText}</strong></small>
                ${getPasswordTips(password)}
            `;
        });
    }

    function getPasswordTips(password) {
        const tips = [];
        if (password.length < 8) tips.push('Минимум 8 символов');
        if (!/[A-Z]/.test(password)) tips.push('Добавьте заглавные буквы');
        if (!/[0-9]/.test(password)) tips.push('Добавьте цифры');
        if (!/[^A-Za-z0-9]/.test(password)) tips.push('Добавьте спецсимволы');
        
        return tips.map(tip => 
            `<small class="text-danger d-block">✗ ${tip}</small>`
        ).join('');
    }

    // 4. Общая валидация формы
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const isNameValid = validateName.call(firstNameInput);
        const isUsernameValid = await validateUsername.call(usernameInput);
        
        if (isNameValid && isUsernameValid) {
            this.submit(); // Если всё valid, отправляем форму
        } else {
            showToast('Пожалуйста, исправьте ошибки в форме');
        }
    });

    // Вспомогательные функции
    function showError(field, message) {
        clearError(field);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        field.classList.add('is-invalid');
        field.parentNode.appendChild(errorDiv);
    }

    function clearError(field) {
        field.classList.remove('is-invalid');
        const oldError = field.parentNode.querySelector('.invalid-feedback');
        if (oldError) oldError.remove();
    }

    function showToast(message) {
        // Реализация простого уведомления
        const toast = document.createElement('div');
        toast.className = 'position-fixed bottom-0 end-0 p-3';
        toast.innerHTML = `
            <div class="toast show" role="alert">
                <div class="toast-body bg-danger text-white">
                    ${message}
                </div>
            </div>
        `;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
});