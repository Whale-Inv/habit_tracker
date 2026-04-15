# Habit Tracker

Приложение для отслеживания привычек с напоминаниями в Telegram.

## Запуск проекта через Docker Compose

### Предварительные требования

- Установленный Docker Desktop
- Установленный Docker Compose

### 1. Клонирование репозитория

```
git clone https://github.com/Whale-Inv/habit-tracker.git
cd habit-tracker
```

### 2. Настройка переменных окружения
Создайте файл `.env` в корне проекта:
```
# Django
SECRET_KEY=your-secret-key-here

# Postgres
POSTGRES_DB=habit_tracker
POSTGRES_USER=habit_user
POSTGRES_PASSWORD=habit_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_API_URL=https://api.telegram.org/bot

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
### 3. Запуск всех сервисов
`docker-compose up --build
`
### 4. Выполнение миграций (первый запуск)
`docker-compose exec web python manage.py migrate`
### 5. Создание суперпользователя
`docker-compose exec web python manage.py createsuperuser`

## Проверка работоспособности сервисов

### Web (Django)
```
# Откройте в браузере
http://localhost:8000

# Проверка API
curl http://localhost:8000/api/habits/

# Админка
http://localhost:8000/admin
```
### База данных (PostgreSQL)
```
# Подключение к БД
docker-compose exec db psql -U habit_user -d habit_tracker

# Проверка таблиц
\dt
\q
```
### Redis
```
# Проверка подключения
docker-compose exec redis redis-cli ping

# Ожидаемый ответ: PONG
```
### Celery Worker
```
# Просмотр логов
docker-compose logs celery

# Ожидаемый вывод:
# celery@... ready.
```
### Celery Beat
```
# Просмотр логов
docker-compose logs celery-beat

# Ожидаемый вывод:
# beat: Starting...
# Scheduler: Sending due task...
```
## Команды для управления
### Выводит список всех контейнеров и их текущее состояние:
`docker-compose ps`
### Остановка всех сервисов
`docker-compose down`
### Перезапуск сервисов
`docker-compose restart`
### Позволяет просматривать логи всех контейнеров
`docker-compose logs`