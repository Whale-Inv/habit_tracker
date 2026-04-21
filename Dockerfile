FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc libpq-dev curl netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

ARG SECRET_KEY=dummy-key-for-build
ENV SECRET_KEY=$SECRET_KEY

RUN python manage.py collectstatic --noinput

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]