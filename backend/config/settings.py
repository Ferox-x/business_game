from os import path, getenv
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = getenv("SECRET_KEY", "secret_key")

DEBUG = int(getenv("DEBUG", False))

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "localhost").split()

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "silk",
    "apps.authenticate",
    "apps.users",
    "apps.business_game",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "silk.middleware.SilkyMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES_DIR = path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [getenv("LOCATION")],
        },
    },
}

DATABASES = {
    "default": {
        "ENGINE": getenv("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        "NAME": getenv("POSTGRES_DB", "postgres"),
        "USER": getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": getenv("DB_HOST", "localhost"),
        "PORT": getenv("DB_PORT", "5432"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": getenv("LOCATION"),
    }
}

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

REST_FRAMEWORK = {
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": ("apps.authenticate.backends.JWTAuthentication",),
    "EXCEPTION_HANDLER": "config.exceptions.core_exception_handler",
}

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "bgames.supp@gmail.com"
EMAIL_HOST_PASSWORD = "axpwukzrjchryhgz"

PHONENUMBER_DEFAULT_REGION = "RU"

LANGUAGES = (
    ("en", _("English")),
    ("ru", _("Russian")),
)

LANGUAGE_CODE = "ru-RU"

LOCALE_PATHS = (path.join(BASE_DIR, "locale"),)

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

INTERNAL_IPS = [
    "127.0.0.1",
]

LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "/"
AUTH_USER_MODEL = "authenticate.AuthUser"

ADMIN_EMAIL = getenv("ADMIN_EMAIL")

# CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r"^/api/.*$"
CORS_ORIGIN_WHITELIST = ("http://localhost:3000",)
#
# CSRF_COOKIE_SAMESITE = 'None'
#
# CSRF_COOKIE_SECURE = True
#
# CSRF_COOKIE_NAME = 'csrftoken'
#
# CORS_ALLOW_CREDENTIALS = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [path.join(BASE_DIR, "static")]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {filename} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": "logs.log",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}
