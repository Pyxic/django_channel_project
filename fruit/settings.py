"""
Django settings for fruit project.

Generated by 'django-fruit_admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-d1j^hm$^f1dos(hsvmwri_&ujiof41e25-)r2m*e6a)@5j7k#z')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", '*').split(" ")


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.fruit_admin',
    'channels',
    'fruit_admin',
    'account',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
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

ROOT_URLCONF = 'fruit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'fruit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE", "django.db.backends.postgresql_psycopg2"),
        'NAME': os.environ.get("SQL_DATABASE", 'fruit'),
        'USER': os.environ.get("SQL_USER", 'postgres'),
        'PASSWORD': os.environ.get("SQL_PASSWORD", 'pass12345'),
        'HOST': os.environ.get("SQL_HOST", '127.0.0.1'),
        'PORT': os.environ.get("SQL_PORT", '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CELERY
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TASK_ROUTES = ([
    ('fruit_admin.tasks.buy_apples', {'queue': 'queue1'}),
    ('fruit_admin.tasks.sell_apples', {'queue': 'queue1'}),
    ('fruit_admin.tasks.buy_bananas', {'queue': 'queue1'}),
    ('fruit_admin.tasks.sell_bananas', {'queue': 'queue1'}),
    ('fruit_admin.tasks.buy_pineapples', {'queue': 'queue1'}),
    ('fruit_admin.tasks.sell_pineapples', {'queue': 'queue1'}),
    ('fruit_admin.tasks.buy_peaches', {'queue': 'queue1'}),
    ('fruit_admin.tasks.sell_peaches', {'queue': 'queue1'}),
    ('fruit_admin.tasks.get_random_joke', {'queue': 'queue1'}),
    ('fruit_admin.tasks.update_stock', {'queue': 'queue2'}),
    ('fruit_admin.tasks.get_updates', {'queue': 'queue2'}),
],)

CELERY_BEAT_SCHEDULE = {
    'buy_apples': {
        'task': 'fruit_admin.tasks.buy_apples',
        'schedule': 6,
        # 'options': {'queue': 'queue1'}
    },
    'sell_apples': {
        'task': 'fruit_admin.tasks.sell_apples',
        'schedule': 15,
        # 'options': {'queue': 'queue1'}
    },
    'buy_bananas': {
        'task': 'fruit_admin.tasks.buy_bananas',
        'schedule': 9,
        # 'options': {'queue': 'queue1'}
    },
    'sell_bananas': {
        'task': 'fruit_admin.tasks.sell_apples',
        'schedule': 12,
        # 'options': {'queue': 'queue1'}
    },
    'buy_pineapples': {
        'task': 'fruit_admin.tasks.buy_pineapples',
        'schedule': 12,
        # 'options': {'queue': 'queue1'}
    },
    'sell_pineapples': {
        'task': 'fruit_admin.tasks.sell_pineapples',
        'schedule': 9,
        # 'options': {'queue': 'queue1'}
    },
    'buy_peaches': {
        'task': 'fruit_admin.tasks.buy_peaches',
        'schedule': 15,
        # 'options': {'queue': 'queue1'}
    },
    'sell_peaches': {
        'task': 'fruit_admin.tasks.sell_peaches',
        'schedule': 6,
        # 'options': {'queue': 'queue1'}
    },
    'get_random_joke': {
        'task': 'fruit_admin.tasks.get_random_joke',
        'schedule': 10,
    },
    'get_updates': {
        'task': 'fruit_admin.tasks.get_updates',
        'schedule': 10,
    }

}

ASGI_APPLICATION = "fruit.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("redis", 6379)]},
    }
}


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
]
