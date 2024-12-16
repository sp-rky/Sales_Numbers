#!/bin/bash

# load all the environment variables into /etc/environment (makes env variables accessible to cronjobs)
printenv > /etc/environment

# start cron at max logging mode
cron -L 15

# start the django server (needs to be changed to run on nginx at some point)
python3 manage.py runserver 0.0.0.0:8000 >> /var/log/django.log
