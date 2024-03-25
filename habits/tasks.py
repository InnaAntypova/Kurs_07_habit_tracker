from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from habits.services import TelegramBot
from users.models import User


@shared_task
def send_habits():
    current_time = timezone.now() + timedelta(hours=3)
    habits = Habit.objects.all()
    bot = TelegramBot()
    for habit in habits:
        if habit.periodicity == habit.Periodicity.DAILY and habit.start_time > current_time + timedelta(seconds=60):
            user = User.objects.get(pk=habit.user.pk)
            text = f'Напоминание о ежедневной привычке:\nЯ буду {habit.action} в {habit.start_time} в {habit.place}'
            bot.send_message(user.telegram_id, text)

        if habit.periodicity == habit.Periodicity.WEEKLY and habit.start_time > current_time + timedelta(days=3):
            user = User.objects.get(pk=habit.user.pk)
            text = f'Напоминание о еженедельной привычке:\nЯ буду {habit.action} в {habit.start_time} в {habit.place}'
            bot.send_message(user.telegram_id, text)
