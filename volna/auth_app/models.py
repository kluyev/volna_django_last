from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLES = (
        ('parent', 'Родитель'),
        ('staff', 'Сотрудник'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='parent')

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: '+79999999999'"
    )
    
    phone = models.CharField(
        'Телефон',
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True
    )
    is_profile_completed = models.BooleanField(
        'Профиль заполнен',
        default=False,
        help_text="Отметьте, если пользователь заполнил профиль"
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    child_health_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
class Child(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мальчик'),
        ('F', 'Девочка'),
    ]
    
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='Родитель'
    )
    first_name = models.CharField(
        'Имя',
        max_length=100,
        help_text="Введите имя ребенка"
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=100,
        help_text="Введите фамилию ребенка"
    )
    birth_date = models.DateField(
        'Дата рождения',
        help_text="Укажите дату рождения в формате ДД.ММ.ГГГГ"
    )
    gender = models.CharField(
        'Пол',
        max_length=1,
        choices=GENDER_CHOICES
    )
    special_needs = models.TextField(
        'Особенности здоровья',
        blank=True,
        help_text="Аллергии, хронические заболевания и т.д."
    )
    created_at = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )

    def age(self):
        import datetime
        return int((datetime.date.today() - self.birth_date).days / 365.25)
    
    class Meta:
        verbose_name = 'Ребенок'
        verbose_name_plural = 'Дети'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.birth_date})"