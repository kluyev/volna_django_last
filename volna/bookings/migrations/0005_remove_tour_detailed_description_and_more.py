# Generated by Django 5.2.1 on 2025-06-07 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_tour_detailed_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tour',
            name='detailed_description',
        ),
        migrations.AlterField(
            model_name='tour',
            name='description',
            field=models.TextField(verbose_name='Короткое описание'),
        ),
    ]
