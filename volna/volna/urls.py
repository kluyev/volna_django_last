from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), # Админка
    path('auth/', include('auth_app.urls')), # Авторизация
    path('', include('core.urls')),          # Главная страница
    path('tours/', include('bookings.urls')), # Путевки
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)