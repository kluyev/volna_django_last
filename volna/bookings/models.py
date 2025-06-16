from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Booking(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открытая'),
        ('completed', 'Завершенная'),
        ('rejected', 'Отклонена')
    )
    
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, verbose_name='Путевка')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Родитель')
    child = models.ForeignKey('auth_app.Child', on_delete=models.CASCADE, verbose_name='Ребенок')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='open',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    rejection_reason = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Причина отклонения'
    )

    def __str__(self):
        return f"Бронирование #{self.id} - {self.tour.title}"
    
    def clean(self):
        # Проверка доступности мест
        if self.status == 'open' and self.tour.available_seats < 1:
            raise ValidationError('Нет свободных мест на эту путевку')
        
        # Проверка что ребенок принадлежит родителю
        if self.child.parent != self.user:
            raise ValidationError('Выбранный ребенок не принадлежит вам')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.pk:
            orig = Booking.objects.get(pk=self.pk)
        else:
            orig = None
        
        # При создании новой брони уменьшаем количество мест
        if not orig and self.status == 'open':
            if self.tour.available_seats > 0:
                self.tour.available_seats -= 1
                self.tour.save()
            else:
                raise ValidationError('Нет свободных мест на эту путевку')
        
        # При изменении статуса с "открыта" на "отклонена" возвращаем место
        if orig and orig.status == 'open' and self.status == 'rejected':
            self.tour.return_seat()
        
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-created_at']

class Tour(models.Model):
    TYPE_CHOICES = (
        ('summer', 'Летняя'),
        ('winter', 'Зимняя'),
        ('season', 'Сезонная'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Короткое описание')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    duration = models.PositiveIntegerField(verbose_name='Длительность (дней)', default=21)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Тип', default='summer')
    image = models.ImageField(upload_to='tours/', verbose_name='Изображение', blank=True)
    available_seats = models.PositiveIntegerField(verbose_name='Свободные места', default=30)
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    program = models.TextField('Программа', help_text='Каждый пункт с новой строки', blank=True)
    includes = models.TextField(
        'Что включено', 
        help_text='Каждый пункт с новой строки', 
        default="""Заглушка"""
    )

    def get_program_items(self):
        return [item.strip() for item in self.program.split('\n') if item.strip()]
    
    def get_includes_items(self):
        return [item.strip() for item in self.includes.split('\n') if item.strip()]
    
    def __str__(self):
        return self.title
    
    def return_seat(self):
        """Возврат места при отмене бронирования"""
        self.available_seats += 1
        self.save()
    
    @property
    def formatted_price(self):
        return f"{self.price} ₽"
    