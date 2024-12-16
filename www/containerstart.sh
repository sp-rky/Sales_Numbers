#!/bin/sh

# load all the environment variables into /etc/environment (makes env variables accessible to cronjobs)
printenv > /etc/environment

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# start cron at max logging mode
cron -L 15

python manage.py migrate

# start the django server
#python3 manage.py runserver 0.0.0.0:8000 >> /var/log/django.log
gunicorn Sales_Numbers.wsgi:application --bind 0.0.0.0:8000

