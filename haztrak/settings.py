"""
Django settings for haztrak project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
if os.getenv('HAZTRAK_SECRET_KEY'):
    SECRET_KEY = os.getenv('HAZTRAK_SECRET_KEY')
else:
    logging.error('environment HAZTRAK_SECRET_KEY not found, exiting')
    exit(1)

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('HAZTRAK_DEBUG'):
    if os.getenv('HAZTRAK_DEBUG').upper() == 'TRUE':
        DEBUG = True
else:
    DEBUG = False

if os.getenv('HAZTRAK_HOST'):
    ALLOWED_HOSTS = os.getenv('HAZTRAK_HOST')
    if type(ALLOWED_HOSTS) is str:
        ALLOWED_HOSTS = [ALLOWED_HOSTS]
else:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'apps.trak',
    'apps.home',
    'apps.accounts',
    'apps.api'
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

ROOT_URLCONF = 'haztrak.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'haztrak.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if os.getenv('DB_NAME'):
    required_env_vars = [
        'DB_ENGINE',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
    ]
    for i in required_env_vars:
        if not os.getenv(i):
            logging.error(f'missing required DB environment variable {i}')
            exit(1)
    if not os.getenv('TEST_DB_NAME'):
        os.environ['test'] = 'test'
    default_db = {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'TEST': {
            'NAME': os.getenv('TEST_DB_NAME')
        }
    }
else:
    logging.info('Resorting to sqlite backend')
    default_db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }

DATABASES = {
    'default': default_db
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

if os.getenv('HAZTRAK_TIMEZONE'):
    TIME_ZONE = os.getenv('HAZTRAK_TIMEZONE')
else:
    TIME_ZONE = 'UTC'

USE_I18N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static/"
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FIXTURE_DIRS = ['tests/fixtures']

# RCRAInfo environment
if not os.getenv('RCRAINFO_ENV'):
    os.environ['RCRAINFO_ENV'] = 'preprod'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
