import os
import logging
from pathlib import Path
from datetime import timedelta

from kombu import Queue, Exchange
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from libs.utils import get_env_variables_list


# Environments
ENVIRONMENT_PRODUCTION = 'production'
ENVIRONMENT_DEVELOPMENT = 'dev'
ENVIRONMENT_LOCAL = 'local'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Boilerplate')
ENVIRONMENT = os.environ.get('ENVIRONMENT', ENVIRONMENT_DEVELOPMENT)
RELEASE = os.environ.get('RELEASE', '0.1')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', 0)))

if ENVIRONMENT == ENVIRONMENT_PRODUCTION:
    DEBUG = False

ALLOWED_HOSTS = get_env_variables_list(env_name='ALLOWED_HOSTS')
CORS_ALLOW_METHODS = get_env_variables_list(env_name='CORS_ALLOW_METHODS')
CORS_ALLOWED_ORIGINS = get_env_variables_list(env_name='CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = get_env_variables_list(env_name='CSRF_TRUSTED_ORIGINS')


# Application definition

INSTALLED_APPS = [
    # Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'apps',

    # Third party apps
    'debug_toolbar',
    'corsheaders',
    'rest_framework',
    'storages',
    'drf_yasg',
    'nested_admin',
    'django_celery_beat',
    'django_celery_results',
]


if DEBUG:
    import socket  # only if you haven't already imported this
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASS'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': int(os.environ.get('POSTGRES_PORT')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DJANGO_SUPERUSER_LOGIN = os.environ.get('DJANGO_SUPERUSER_LOGIN', 'admin')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# S3
USE_S3 = bool(int(os.environ.get('USE_S3')))
if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # s3 static settings
    PUBLIC_MEDIA_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'settings.storages.MediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'

    # s3 media settings
    PUBLIC_STATIC_LOCATION = 'backend-static'
    STATICFILES_STORAGE = 'settings.storages.StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_STATIC_LOCATION}/'
else:
    STATIC_DIR = 'backend-static'
    STATIC_URL = f'/api/{STATIC_DIR}/'
    STATIC_ROOT = os.path.join(BASE_DIR, STATIC_DIR)

    MEDIA_DIR = 'media'
    MEDIA_URL = f'/api/{MEDIA_DIR}/'
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF yasg settings (api documentation)
# https://drf-yasg.readthedocs.io/en/stable/settings.html

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'REFETCH_SCHEMA_WITH_AUTH': True,
    'USE_SESSION_AUTH': False,
    'PERSIST_AUTH': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            "format": "[{asctime} {levelname} {pathname}.{funcName}:{lineno}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{asctime} {levelname} {funcName}:{lineno}] {message}",
            "style": "{",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            "formatter": "verbose",
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
SENTRY_ENVIRONMENT = ENVIRONMENT
SENTRY_RELEASE = RELEASE

sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=SENTRY_ENVIRONMENT,
    release=SENTRY_RELEASE,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[
        DjangoIntegration(
            transaction_style='url',
            middleware_spans=True,
            signals_spans=False,
            cache_spans=False,
        ),
        LoggingIntegration(
            level=logging.INFO,
            event_level=logging.WARNING,
        ),
    ]
)


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379')
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = int(os.environ.get('CELERY_TASK_TIME_LIMIT_MIN', 5)) * 60

CELERY_DEFAULT_QUEUE_NAME = 'default'

CELERY_QUEUES = [
    Queue(
        CELERY_DEFAULT_QUEUE_NAME,
        Exchange(CELERY_DEFAULT_QUEUE_NAME),
        routing_key=CELERY_DEFAULT_QUEUE_NAME,
    ),
]

CELERY_IMPORTS = (
    # 'apps.app.tasks',
)

CELERY_TASK_DEFAULT_QUEUE = CELERY_DEFAULT_QUEUE_NAME

CELERY_ROUTES = dict()
CELERY_BEAT_SCHEDULE = dict()


# scheduled tasks
# create boolean SWITCHER_ENV to enable/disable tasks
# create int SCHEDULE_ENV to define schedule for task in seconds
if bool(int(os.environ.get('SWITCHER_ENV', '0'))):
    CELERY_BEAT_SCHEDULE.update({
        'twitter-update-followers-stats': {
            'task': 'apps.stats.twitter.tasks.count_followers_stats',
            'schedule': timedelta(seconds=int(os.environ.get('SCHEDULE_ENV', 60))),
            'options': {
                'queue': CELERY_TASK_DEFAULT_QUEUE,
            },
        }
    })
