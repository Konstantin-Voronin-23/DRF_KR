#!/bin/sh

echo "Waiting for database..."
while ! python manage.py check --database default >/dev/null 2>&1; do
    echo "Database not ready, waiting..."
    sleep 5
done

echo "Database is ready!"
echo "Running migrations..."
python manage.py migrate

echo "Starting Celery Beat..."
celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
