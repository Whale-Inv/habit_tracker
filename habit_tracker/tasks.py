from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habit_tracker.models import Habit
from habit_tracker.services import send_telegram_message


@shared_task
def check_upcoming_habits():
    """
        Проверяет привычки, которые нужно выполнить через 15 минут
    """
    now = timezone.now()
    reminder_time = now + timedelta(minutes=15)

    habits = Habit.objects.all()

    for habit in habits:

        if (
                habit.habit_time.date() == reminder_time.date() and
                habit.habit_time.hour == reminder_time.hour and
                habit.habit_time.minute == reminder_time.minute
        ):
            if habit.creator.telegram_chat_id:
                message = f"🔔 Через 15 минут: {habit.habit_action} в {habit.habit_place}"
                send_telegram_message(habit.creator.telegram_chat_id, message)
