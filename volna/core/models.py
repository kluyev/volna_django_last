from django.db import models

class ContactRequest(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('completed', 'Завершена'),
    )

    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Заявка от {self.name} ({self.created_at})"