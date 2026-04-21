# Habit Tracker

Приложение для отслеживания привычек с напоминаниями в Telegram.

## Демо

Приложение развернуто и доступно по адресу:  
**http://103.76.53.62**

- Админка: http://103.76.53.62/admin
- API: http://103.76.53.62/habits/

---

## Содержание

- [Локальный запуск](#локальный-запуск)
- [Настройка удаленного сервера](#настройка-удаленного-сервера)
- [CI/CD GitHub Actions](#cicd-github-actions)
- [Команды для управления](#команды-для-управления)
- [Проверка работоспособности](#проверка-работоспособности)

---

## Локальный запуск

### Требования

- Docker Desktop
- Git

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

## Настройка удаленного сервера

### 1. Подготовка сервера (Ubuntu 24.04)
```commandline
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker

# Настройка firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

### 2. Настройка SSH-ключей
На локальной машине:
```commandline
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_actions -N ""
ssh-copy-id -i ~/.ssh/github_actions.pub test@103.76.53.62
```
### 3. Клонирование и запуск на сервере
```commandline
ssh test@103.76.53.62
git clone -b develop https://github.com/Whale-Inv/habit-tracker.git habit-tracker
cd habit-tracker
cp .env.template .env
nano .env  # заполните переменные
docker compose up -d --build
docker exec -it habit_tracker-web-1 python manage.py createsuperuser
```
## CI/CD GitHub Actions
### Как это работает
При каждом push в ветку `develop` автоматически запускается:
```commandline
push → develop
    ↓
1. Линтер (flake8) → проверка стиля кода
    ↓
2. Тесты (Django) → запуск всех тестов
    ↓
3. Сборка Docker образа → push в Docker Hub
    ↓
4. Деплой на сервер → обновление контейнеров
```
### Настройка GitHub Secrets
В репозитории: **Settings** → **Secrets and variables** → **Actions**

| Secret          | Описание                           |
|-----------------|------------------------------------|
| DOCKER_USERNAME | 	Имя пользователя Docker Hub       |
| DOCKER_PASSWORD | 	Токен доступа Docker Hub          |
| SERVER_HOST     | 	IP адрес сервера (103.76.53.62)   |
| SERVER_USER	    | Имя пользователя на сервере (test) |
| SSH_PRIVATE_KEY | 	Приватный SSH ключ                |

### Файл workflow
`.github/workflows/deploy.yml` содержит:
* **Linter**: flake8 проверка кода
* **Tests**: Django тесты (на SQLite для скорости)
* **Build**: сборка Docker образа и пуш в Docker Hub
* **Deploy**: SSH на сервер → `docker pull` → `docker compose up -d`

### Команды для управления

| Команда	                 | Действие                       |
|--------------------------|--------------------------------|
| docker compose ps	       | Список контейнеров и их статус |
| docker compose logs	     | Логи всех контейнеров          |
| docker compose logs web	 | Логи Django приложения         |
| docker compose restart	  | Перезапуск всех сервисов       |
| docker compose down	     | Остановка всех сервисов        |
| docker compose up -d	    | Запуск в фоновом режиме        |

### Проверка работоспособности
```commandline
# Откройте в браузере
http://103.76.53.62/habits/
http://103.76.53.62/admin/
```

## Автор
### Nikita Dorozhko
* **GitHub**: [@Whale-Inv](https://github.com/Whale-Inv)
* **Docker Hub**: [exzently](https://hub.docker.com/u/exzently)

## Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).  
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)