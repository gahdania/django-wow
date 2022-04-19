from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = config("SECRET_KEY", default="django-insecure$settings.local")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.users.apps.AccountsConfig",
    "apps.forums.apps.ForumsConfig",
    "apps.core.apps.CoreConfig",
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "urls"

INTERNAL_IPS = ["127.0.0.1"]

WSGI_APPLICATION = "wsgi.application"

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'users/login_user/'
LOGIN_REDIRECT_URL = 'users/profile/'

# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "apps.core.context_processors.guild_string",
            ],
        },
    },
]


# ==============================================================================
# Authentication Backends
# ==============================================================================


# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ==============================================================================
# I18N AND L10N SETTINGS
# ==============================================================================

LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")

TIME_ZONE = config("TIME_ZONE", default="UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_URL = "/static/"

# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = "/media/"

GUILD = 'Thanks I Hate It'
REALM = 'Zul\'jin'
REGION = 'US'


CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')

AUTHLIB_OAUTH_CLIENTS = {
    'battlenet': {
        'client_id': config('CLIENT_ID'),
        'client_secret': config('CLIENT_SECRET'),
    }
}


