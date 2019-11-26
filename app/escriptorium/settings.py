"""
Django settings for escriptorium project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = [('Robin Tissot','tissotrobin@gmail.com'),]

# Add apps directory the sys.path
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.append(APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'a-beautiful-snowflake')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = ['*']

ASGI_APPLICATION = "escriptorium.routing.application"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',

    'django_cleanup',
    'ordered_model',
    'easy_thumbnails',
    'channels',
    'rest_framework',
    
    'bootstrap',
    'versioning',
    'users',
    'core',
    'imports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'escriptorium.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates'),],
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

WSGI_APPLICATION = 'escriptorium.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.getenv('SQL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('POSTGRES_DB', os.path.join(BASE_DIR, 'escriptorium')),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('SQL_HOST', 'localhost'),
        'PORT': os.getenv('SQL_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'documents-list'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
from django.utils.translation import gettext_lazy as _
LANGUAGES = [
  ('en', _('English')),
  ('de', _('French')),
]

EMAIL_HOST = 'mail'
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'no-reply@escriptorium.fr'

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%d/1" % (REDIS_HOST, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "cache"
    }
}

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_HOST', 9200)

CELERY_BROKER_URL = 'redis://%s:%d/0' % (REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://%s:%d' % (REDIS_HOST, REDIS_PORT)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# time in seconds a user has to wait after a task is started before being able to recover
TASK_RECOVER_DELAY = 60 * 60 * 24  # 1 day
from kombu import Queue, Exchange

CELERY_TASK_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('img-processing', routing_key='img-processing'),
    Queue('low-priority', Exchange('low-priority'), routing_key='low-priority'),
)
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_ROUTES = {
    'core.tasks.*': {'queue': 'img-processing'},
    'core.tasks.train': {'queue': 'low-priority'},
    'core.tasks.lossless_compression': {'queue': 'low-priority'},
    'core.tasks.generate_part_thumbnails': {'queue': 'low-priority'},
    #'escriptorium.celery.debug_task': '',
    'imports.tasks.*': {'queue': 'low-priority'},
    #'users.tasks.async_email': '',
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}
# fixes https://github.com/django/channels/issues/1240:
DATA_UPLOAD_MAX_MEMORY_SIZE = 150*1024*1024 # value in bytes (so 150Mb)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs', 'error.log'),
        },

        'kraken_logs': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs', 'kraken', 'train.log'),
        },
        
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'kraken':{
            'handlers': ['kraken_logs', 'console'],
            'propagate': True
        },
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
        },
        'core': {
            'handlers': ['file', 'console'],
            'propagate': True,
        }
    },
}

COMPRESS_ENABLE = True

THUMBNAIL_ENABLE = True
THUMBNAIL_ALIASES = {
    '': {
        'list': {'size': (50, 50), 'crop': 'center'},
        'card': {'size': (180, 180), 'crop': 'center'},
        'large': {'size': (1110, 0), 'crop': 'scale', 'upscale': False}
    }
}
THUMBNAIL_OPTIMIZE_COMMAND = {
    # 'png': '/usr/bin/optipng {filename}',
    # 'gif': '/usr/bin/optipng {filename}',
    'jpeg': '/usr/bin/jpegoptim {filename}'
}

VERSIONING_DEFAULT_SOURCE = 'eScriptorium'

IIIF_IMPORT_QUALITY = 'full'

KRAKEN_TRAINING_DEVICE = 'cpu'  # or cuda
KRAKEN_DEFAULT_SEGMENTATION_MODEL = os.path.join(APPS_DIR, 'core/static/offsplit.mlmodel')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomPagination',
    'PAGE_SIZE': 10,
}

if 'test' in sys.argv:
    try:
        from .test_settings import *
    except (ModuleNotFoundError, ImportError):
        pass
