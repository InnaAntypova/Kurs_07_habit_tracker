from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """ Модель для сущности Habit (Привычка)"""

    class Periodicity(models.TextChoices):
        DAILY = 'Ежедневно', 'Daily'
        WEEKLY = 'Еженедельно', 'Weekly'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=150, verbose_name='Место выполнения')
    action = models.CharField(max_length=150, verbose_name='Действие')
    is_nice = models.BooleanField(verbose_name='Признак приятной привычки')
    associated = models.ForeignKey('self', verbose_name='Связанная привычка', on_delete=models.CASCADE, **NULLABLE)
    periodicity = models.CharField(choices=Periodicity.choices, default=Periodicity.DAILY, verbose_name='Периодичность')
    fee = models.CharField(max_length=150, verbose_name='Вознаграждение', **NULLABLE)
    start_time = models.DateTimeField(verbose_name='Время')
    execution_time = models.DateTimeField(verbose_name='Время на выполнение')
    is_published = models.BooleanField(verbose_name='Признак публичности')

    def __str__(self):
        return f'Habit: {self.user}/{self.place}/{self.is_nice}/{self.is_published} Associated:({self.associated})'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
