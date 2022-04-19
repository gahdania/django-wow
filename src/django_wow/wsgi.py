"""
WSGI config for src project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from decouple import config

from django.core.wsgi import get_wsgi_application


project_env = os.environ.get('PROJECT_ENV')
if not project_env:
    project_env = config('PROJECT_ENV', default='local')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'django_wow.settings.{project_env}')


application = get_wsgi_application()
