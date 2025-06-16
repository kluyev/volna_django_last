from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ParentProfile, Child
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

class ParentRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Ваше имя*",
        max_length=25,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Иван'
        }),
        error_messages={
            'required': 'Обязательное поле',
            'max_length': 'Слишком длинное имя (макс. 25 символов)'
        }
    )
    
    username = forms.CharField(
        label="Логин*",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Придумайте логин'
        }),
        help_text="Только буквы, цифры и (@ . + - _ )"
    )
    
    password1 = forms.CharField(
        label="Пароль*",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password-input',
            'placeholder': 'Не менее 8 символов'
        }),
        help_text="<div id='password-strength'></div>"
    )
    
    password2 = forms.CharField(
        label="Подтверждение пароля*",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[\w.@+-]+$', username):
            raise ValidationError("Недопустимые символы в логине")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name.strip()) < 2:
            raise ValidationError("Имя слишком короткое")
        return first_name.strip()

class ParentProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            pattern = re.compile(r'^\+?1?\d{9,15}$')
            if not pattern.match(phone):
                raise ValidationError("Неверный формат телефона. Пример: +79999999999")
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("Введите корректный email адрес")
        return email

    class Meta:
        model = User
        fields = ['last_name', 'phone', 'email']
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванов'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+79999999999'
            }),
        }
        labels = {
            'last_name': 'Фамилия',
            'phone': 'Телефон',
            'email': 'Email адрес'
        }
        help_texts = {
            'phone': 'Номер телефона будет использоваться для экстренных уведомлений',
        }

class ChildForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['birth_date'].widget.attrs.update({
            'type': 'date'
        })
        self.fields['special_needs'].widget.attrs.update({
            'rows': 3
        })
    
    def clean_birth_date(self):
        from datetime import date
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise ValidationError("Дата рождения не может быть в будущем")
        return birth_date

    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'special_needs']
        labels = {
            'first_name': 'Имя ребенка',
            'last_name': 'Фамилия ребенка',
            'gender': 'Пол',
            'birth_date': 'Дата рождения',
            'special_needs': 'Особенности здоровья'
        }

class ParentLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.role == 'parent':
            raise forms.ValidationError(
                "Доступ только для родителей",
                code='invalid_role',
            )
        
class StaffLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.role in ['staff', 'admin']:
            raise forms.ValidationError(
                "Доступ только для сотрудников",
                code='invalid_role',
            )