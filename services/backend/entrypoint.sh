#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate --no-input
python manage.py collectstatic --no-input

# setup commands
python manage.py create_default_super_user

gunicorn settings.wsgi:application --reload --bind 0.0.0.0:8000 --workers 4 --timeout 300
