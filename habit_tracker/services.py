import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    """
        Отправка напоминания в телеграм бот
    """
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    requests.get(f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage", params=params)
