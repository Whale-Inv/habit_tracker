FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml poetry.lock README.md ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копирование проекта
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]