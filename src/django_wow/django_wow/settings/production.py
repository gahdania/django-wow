# flake8: noqa
import os

import dj_database_url
import sentry_sdk
from celery.schedules import crontab
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True


# ==============================================================================
# THIRD-PARTY APPS SETTINGS
# ==============================================================================

sentry_sdk.init(
    dsn=config("SENTRY_DSN", default=None),
    environment=f"Danjgo WoW: {os.environ.get('PROJECT_ENV')}",
    release="0.0.1",
    integrations=[DjangoIntegration()],
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config("CACHE_BACKEND", default='redis://localhost:6379'),
        'OPTIONS': {
            'db': '10',
            'parser_class': 'redis.connection.PythonParser',
            'pool_class': 'redis.BlockingConnectionPool',
        }
    }
}

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="postgres://django_wow:django_wow@localhost:5432/django_wow"),
        conn_max_age=600,
    )
}
# CELERY

CELERY_ALWAYS_EAGER = True
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='amqp://localhost:5672')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379')

CELERY_BEAT_SCHEDULE = {
    'class-update': {
        'task': 'apps.core.tasks.class_update',
        'schedule': crontab(minute=10, hour=0, day_of_week=4),
        'options': {
            'expires': 15.0,
        },
    },
    'spec-update': {
        'task': 'apps.core.tasks.spec_update',
        'schedule': crontab(minute=11, hour=0, day_of_week=4),
        'options': {
            'expires': 15.0,
        },
    },
    'race-update': {
        'task': 'apps.core.tasks.race_update',
        'schedule': crontab(minute=12, hour=0, day_of_week=4),
        'options': {
            'expires': 15.0,
        },
    },
    'realm-type-update': {
        'task': 'apps.core.tasks.realm_type_update',
        'schedule': crontab(minute=13, hour=0, day_of_week=4),
        'args': (('NORMAL', 'tichondrius'), ('RP', 'argent dawn')),
        'options': {
            'expires': 15.0,
        },
    }

}
