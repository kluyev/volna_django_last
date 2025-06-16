from django.urls import path
from .views import StaffLoginView, parent_profile, ParentLoginView, parent_dashboard, children_list, delete_child, CustomPasswordChangeView, staff_dashboard, staff_request_detail, staff_requests
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from .models import User
from . import views

def check_username(request):
    username = request.GET.get('username', '')
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'exists': exists})

urlpatterns = [
    path('login/', ParentLoginView.as_view(), name='parent_login'),
    path('register/', views.parent_register, name='parent_register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('check_username/', check_username, name='check_username'),
    path('dashboard/', parent_dashboard, name='parent_dashboard'),
    path('profile/', parent_profile, name='parent_profile'),
    path('children/', children_list, name='children_list'),
    path('children/<int:pk>/delete/', delete_child, name='delete_child'),
    path('staff/login/', StaffLoginView.as_view(), name='staff_login'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('staff/requests/', staff_requests, name='staff_requests'),
    path('staff/requests/<int:pk>/', staff_request_detail, name='staff_request_detail'),
    path('bookings/', views.parent_bookings, name='parent_bookings'),
    path('staff/bookings/', views.staff_bookings, name='staff_bookings'),
    path('staff/bookings/update/<int:booking_id>/', views.update_booking_status, name='update_booking_status'), 

    path('password-change/',
         CustomPasswordChangeView.as_view(),
         name='password_change'),

    path('password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='auth_app/parent/password_change_done.html'
        ),
        name='password_change_done'),
]