from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'price', 'available_seats')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'type', 'image', 'price')
        }),
        ('Даты', {
            'fields': ('start_date', 'end_date', 'duration',)
        }),
        ('Описания', {
            'fields': ('description', 'program', 'includes'),
            'classes': ('wide',)
        }),
    )