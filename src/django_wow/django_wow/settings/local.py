# flake8: noqa

from .base import *
import dj_database_url


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

