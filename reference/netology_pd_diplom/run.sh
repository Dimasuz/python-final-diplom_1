#!/bin/sh

python manage.py collectstatic --noinput --clear

python manage.py makemigrations backend

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

gunicorn netology_pd_diplom.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

exec "$@"