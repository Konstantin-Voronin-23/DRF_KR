FROM python:3.12-slim

# Системные зависимости для psycopg2, pillow и др.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev libjpeg-dev zlib1g-dev libpng-dev \
    locales \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY wait_for_db.sh /app/wait_for_db.sh
RUN chmod +x /app/wait_for_db.sh

COPY . /app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Команда для web-сервиса
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
