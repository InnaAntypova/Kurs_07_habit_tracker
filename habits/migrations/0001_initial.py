# Generated by Django 5.0.3 on 2024-03-24 10:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=150, verbose_name='Место выполнения')),
                ('action', models.CharField(max_length=150, verbose_name='Действие')),
                ('is_nice', models.BooleanField(verbose_name='Признак приятной привычки')),
                ('periodicity', models.CharField(choices=[('Ежедневно', 'Daily'), ('Еженедельно', 'Weekly')], default='Ежедневно', verbose_name='Периодичность')),
                ('fee', models.CharField(blank=True, max_length=150, null=True, verbose_name='Вознаграждение')),
                ('start_time', models.DateTimeField(verbose_name='Время')),
                ('execution_time', models.DateTimeField(verbose_name='Время на выполнение')),
                ('is_published', models.BooleanField(verbose_name='Признак публичности')),
                ('associated', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habits.habit', verbose_name='Связанная привычка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
            },
        ),
    ]
