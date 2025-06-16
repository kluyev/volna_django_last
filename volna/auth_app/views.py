from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.urls import reverse
from bookings.models import Booking
from .decorators import staff_required
from core.models import ContactRequest
from .forms import ParentRegisterForm, ParentProfileForm, ParentLoginForm, ChildForm, StaffLoginForm
from .models import User, ParentProfile, Child


@login_required
def parent_dashboard(request):
    """Главная страница личного кабинета"""
    return render(request, 'auth_app/parent/dashboard.html', {
        'active_tab': 'dashboard'
    })

@login_required
def parent_profile(request):
    """Редактирование профиля родителя"""
    if request.method == 'POST':
        form = ParentProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_profile_completed = True
            user.save()
            messages.success(request, 'Профиль успешно сохранен')
            return redirect('parent_profile')
    else:
        form = ParentProfileForm(instance=request.user)
    
    return render(request, 'auth_app/parent/parent_profile.html', {
        'form': form,
        'profile_completed': request.user.is_profile_completed,
        'active_tab': 'profile'
    })

@login_required
def children_list(request):
    """Список детей с возможностью добавления"""
    children = Child.objects.filter(parent=request.user)  # Используем явный фильтр
    show_form = 'add_child' in request.GET
    
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = request.user
            child.save()
            messages.success(request, 'Ребенок успешно добавлен')
            return redirect('children_list')  # Редирект на ту же страницу
    else:
        form = ChildForm() if show_form else None
    
    return render(request, 'auth_app/parent/children_list.html', {
        'children': children,
        'form': form,
        'show_form': show_form,
        'active_tab': 'children'
    })

@login_required
def delete_child(request, pk):
    """Удаление ребенка"""
    child = get_object_or_404(Child, pk=pk, parent=request.user)
    if request.method == 'POST':
        child.delete()
        messages.success(request, 'Ребенок удален из вашего профиля')
    return redirect('children_list')

def parent_register(request):
    if request.method == 'POST':
        user_form = ParentRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'parent'
            user.save()
            
            # Создаем пустой профиль
            ParentProfile.objects.create(user=user)
            
            login(request, user)
            return redirect('parent_profile')
    else:
        user_form = ParentRegisterForm(initial=None)
    
    return render(request, 'auth_app/parent/parent_register.html', {'form': user_form})

class ParentLoginView(LoginView):
    template_name = 'auth_app/parent/parent_login.html'
    form_class = ParentLoginForm
    redirect_authenticated_user = True  # Перенаправляет уже авторизованных пользователей

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'auth_app/parent/password_change.html'
    success_url = '/auth/password-change/done/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'password_change'  # Добавляем активную вкладку
        return context

class StaffLoginView(LoginView):
    template_name = 'auth_app/staff/staff_login.html'
    form_class = StaffLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('staff_dashboard')
    
@staff_required
def staff_dashboard(request):
    if request.user.role not in ['staff', 'admin']:
        return redirect('home')
    
    new_requests = ContactRequest.objects.filter(status='new').count()
    
    return render(request, 'auth_app/staff/dashboard.html', {
        'active_tab': 'dashboard',
        'new_requests': new_requests
    })

@staff_required
def staff_request_detail(request, pk):
    request_obj = get_object_or_404(ContactRequest, pk=pk)
    
    if request.method == 'POST':
        # Логика обработки формы изменения статуса
        pass
    
    return render(request, 'auth_app/staff/request_detail.html', {
        'request': request_obj,
        'active_tab': 'requests'
    })

@login_required
def staff_requests(request):
    if request.user.role not in ['staff', 'admin']:
        return redirect('home')
    
    requests = ContactRequest.objects.all().order_by('-created_at')
    
    return render(request, 'auth_app/staff/requests.html', {
        'active_tab': 'requests',
        'requests': requests
    })

@login_required
def parent_bookings(request):
    """Список бронирований родителя"""
    bookings = Booking.objects.filter(user=request.user).select_related('tour', 'child')
    return render(request, 'auth_app/parent/bookings_list.html', {
        'bookings': bookings,
        'active_tab': 'bookings'
    })

@staff_required
def staff_bookings(request):
    """Список всех бронирований для сотрудника"""
    bookings = Booking.objects.all().select_related('tour', 'user', 'child')
    return render(request, 'auth_app/staff/bookings_list.html', {
        'bookings': bookings,
        'active_tab': 'bookings'
    })

@staff_required
def update_booking_status(request, booking_id):
    """Обновление статуса бронирования"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', '')
        
        # Проверка обязательного комментария при отклонении
        if new_status == 'rejected' and not rejection_reason.strip():
            messages.error(request, 'При отклонении заявки необходимо указать причину')
            return redirect('update_booking_status', booking_id=booking_id)
        
        if new_status in dict(Booking.STATUS_CHOICES).keys():
            # Сохраняем оригинальный статус для обработки возврата мест
            original_status = booking.status
            booking.status = new_status
            
            # Сохраняем причину отклонения
            if new_status == 'rejected':
                booking.rejection_reason = rejection_reason
            
            booking.save()
            
            messages.success(request, 'Статус бронирования обновлен')
            return redirect('staff_bookings')
    
    return render(request, 'auth_app/staff/update_booking_status.html', {
        'booking': booking,
        'active_tab': 'bookings'
    })