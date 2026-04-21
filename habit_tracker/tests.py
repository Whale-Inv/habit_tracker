from datetime import timedelta
from unittest import TestCase
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from habit_tracker.models import Habit
from habit_tracker.tasks import check_upcoming_habits


class HabitTestCase(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(username="test", password="testpass123")

        self.test_habit_time = "2026-04-10T20:30:00.731013+04:00"
        self.reminder_time = "2026-04-10T20:45:00.731013+04:00"

        self.related_habit = Habit.objects.create(
            creator=self.user,
            habit_place="home",
            habit_time=self.reminder_time,
            habit_action="eat apple",
            sign_of_pleasant_habit=True,
            execution_duration="01:30",
            is_public=True,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        data = {
            "habit_place": "home",
            "habit_time": self.reminder_time,
            "habit_action": "test action",
            "related_habit": 1,
            "execution_duration": "01:30",
            "is_public": True,
        }
        response = self.client.post("/habit/create/", data=data)

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "habit_place": "home",
                "habit_time": "2026-04-10T20:45:00.731013+04:00",
                "habit_action": "test action",
                "sign_of_pleasant_habit": False,
                "periodicity": 1,
                "reward": None,
                "execution_duration": "00:01:30",
                "is_public": True,
                "creator": 1,
                "related_habit": 1,
            },
        )


class CheckUpcomingHabitsTaskTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test@test.com", password="testpass123"
        )
        self.user.telegram_chat_id = "123456789"
        self.user.save()

        now = timezone.now()
        self.test_habit_time = now + timedelta(minutes=15)
        self.reminder_time = now + timedelta(minutes=30)

    def test_habit_found_15_minutes_before(self):
        """Привычка за 15 минут до выполнения должна быть найдена"""

        habit = Habit.objects.create(
            creator=self.user,
            habit_place="Home",
            habit_time=self.test_habit_time,
            habit_action="Test habit",
            execution_duration=timedelta(seconds=60),
            is_public=False,
            periodicity=1,
        )

        with patch("habit_tracker.tasks.send_telegram_message") as mock_send:
            result = check_upcoming_habits()

            # Проверяем, что сообщение было отправлено
            mock_send.assert_called_once_with(
                "123456789", "🔔 Через 15 минут: Test habit в Home"
            )
            self.assertEqual(result, None)
            self.assertIsNotNone(habit)


class CheckUpcomingHabitsTaskTest1(TestCase):

    def test_task_called_via_celery(self):
        """Задача может быть вызвана через Celery"""
        with patch("habit_tracker.tasks.check_upcoming_habits.delay") as mock_delay:
            # Вызываем задачу
            check_upcoming_habits.delay()

            mock_delay.assert_called_once()
