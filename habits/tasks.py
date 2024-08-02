import datetime
from celery import shared_task
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_reminder():
    """Отправляет напоминание пользователю о его привычке"""

    habits = Habit.objects.all()
    for habit in habits:
        if habit.start_time == datetime.datetime.now().time():
            send_telegram_message(habit.owner.telegram_id, f"Напоминаю вам о вашей привычке: {habit.action}")