from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from decouple import config

project_env = config('PROJECT_ENV', default='local')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f"django_wow.settings.{project_env}")

app = Celery('django_wow')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
