"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aed!953ui*o%e3mhx4$9sk5l8zez@88!v(s%&lh0jot=7e#xo2'
#SECRET_KEY = os.environ['SECRET_KEY']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["104.248.46.248"]


# Application definition

INSTALLED_APPS = ['career.apps.CareerConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
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

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/Users/tarantim/Dropbox/LiClipse Workspace/test/mysite/career/templates'],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
     #           'ENGINE': 'django.db.backends.postgresql_psycopg2',
     #   'NAME': 'careerday',
     #   'USER': 'c_career',
     #   'PASSWORD': 'tetsuo792',
     #   'HOST': 'localhost',
     #   'PORT': '',
       'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

AWS_ACCESS_KEY_ID = 'RPIBQG3DPFHSGPEKIXSI'
AWS_SECRET_ACCESS_KEY = 'e+SvUUoKa3S61BF020aOzOmvRFZz3MRb7YfmytlTiEs'
AWS_STORAGE_BUCKET_NAME = 'accessspace'
AWS_S3_ENDPOINT_URL = 'https://ams3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = '.'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'career/static'),
]
STATIC_URL = 'https://%s/%s/static/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_ROOT = '/home/career/careerday/media/'
MEDIA_URL = 'https://%s/%s/media/'

#STATIC_URL = '/static/'
#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
