#!/bin/bash
set -e

if [ "$1" = "web" ]; then
  echo "🔄 Running Django migrations..."
  python manage.py migrate --noinput

  echo "🚀 Starting Gunicorn..."
  exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
elif [ "$1" = "celery" ]; then
  echo "📦 Starting Celery worker..."
  exec celery -A config worker --loglevel=INFO
elif [ "$1" = "beat" ]; then
  echo "⏰ Starting Celery beat..."
  exec celery -A config beat --loglevel=INFO
else
  echo "❓ Unknown command: $1"
  exec "$@"
fi
