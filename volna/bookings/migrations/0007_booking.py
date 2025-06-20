# Generated by Django 5.2.1 on 2025-06-11 02:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0006_remove_parentprofile_child_age_and_more'),
        ('bookings', '0006_alter_tour_includes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', 'Открытая'), ('completed', 'Завершенная')], default='open', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.child', verbose_name='Ребенок')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.tour', verbose_name='Путевка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Родитель')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'ordering': ['-created_at'],
            },
        ),
    ]
