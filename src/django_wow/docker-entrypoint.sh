#!/bin/sh

/bin/celery -A django_wow beat -l WARNING
/bin/celery -A django_wow worker -l WARNING
/bin/gunicorn -w 4 -b:8000 --env DJANGO_SETTINGS_MODULE=django_wow.settings.production wsgi:application

