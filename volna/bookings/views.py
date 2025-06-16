from django.shortcuts import render, redirect, get_object_or_404
from .models import Tour, Booking
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auth_app.models import Child

@login_required
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id, is_active=True)
    children = Child.objects.filter(parent=request.user)
    
    if not children.exists():
        messages.warning(request, 'Для бронирования сначала добавьте ребенка в профиль')
        return redirect('children_list')
    
    if request.method == 'POST':
        child_id = request.POST.get('child')
        child = get_object_or_404(Child, id=child_id, parent=request.user)
        
        # Создаем бронирование
        try:
            Booking.objects.create(
                tour=tour,
                user=request.user,
                child=child
            )
            messages.success(request, 'Путевка успешно забронирована!')
            return redirect('parent_bookings')
        except Exception as e:
            messages.error(request, f'Ошибка бронирования: {str(e)}')
    
    return render(request, 'bookings/booking_form.html', {
        'tour': tour,
        'children': children
    })

def tour_list(request):
    # Получаем параметры фильтрации из GET-запроса
    tour_type = request.GET.get('type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    duration = request.GET.get('duration', '')
    
    # Фильтрация путевок
    tours = Tour.objects.filter(is_active=True)
    
    if tour_type:
        tours = tours.filter(type=tour_type)
    
    if min_price:
        tours = tours.filter(price__gte=min_price)
    
    if max_price:
        tours = tours.filter(price__lte=max_price)
    
    if duration:
        tours = tours.filter(duration=duration)
    
    # Для фильтров в шаблоне
    tour_types = Tour.TYPE_CHOICES
    durations = [14, 21, 28]
    
    return render(request, 'bookings/tour_list.html', {
        'tours': tours,
        'tour_types': tour_types,
        'durations': durations,
        'selected_type': tour_type,
        'selected_min': min_price,
        'selected_max': max_price,
        'selected_duration': duration
    })