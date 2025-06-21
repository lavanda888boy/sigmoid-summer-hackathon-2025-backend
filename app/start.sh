#!/bin/sh
set -e

# Use PORT environment variable provided by Cloud Run, fallback to 8080
PORT=${PORT:-8080}

echo "Starting on port: $PORT"

# echo "Applying migrations..."
# python manage.py migrate

echo "Starting Gunicorn server on port $PORT..."
exec gunicorn app.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2