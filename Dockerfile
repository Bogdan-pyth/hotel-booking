FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi --no-root

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]