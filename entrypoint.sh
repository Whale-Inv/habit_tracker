#!/bin/bash

# Ждём PostgreSQL
while ! nc -z db 5432; do
    echo "Waiting for PostgreSQL..."
    sleep 1
done

# Ждём Redis
while ! nc -z redis 6379; do
    echo "Waiting for Redis..."
    sleep 1
done

# Применяем миграции
python manage.py migrate --noinput

# Запускаем Gunicorn
exec gunicorn config.wsgi:application -w 4 -b 0.0.0.0:8000