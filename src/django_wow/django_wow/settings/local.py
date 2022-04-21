# flake8: noqa

from .base import *
import dj_database_url
from celery.schedules import crontab


INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

MEDIA_ROOT = BASE_DIR / "media"

STATIC_DIRS = [
    BASE_DIR / "apps" / "core" / "static",
    BASE_DIR / "static",
]


# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"


DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="postgres://django_wow:django_wow@localhost:5432/django_wow"),
        conn_max_age=600,
    )
}


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
        'schedule': crontab(minute='*/5', hour=0, day_of_week=4),
        'args': (('NORMAL', 'tichondrius'), ('RP', 'argent dawn')),
        'options': {
            'expires': 15.0,
        },
    },
    'character-update': {
        'task': 'apps.core.tasks.character_update',
        'schedule': crontab(minute='*/2'),
        'options': {
            'expires': 15.0,
        },
    }
}
