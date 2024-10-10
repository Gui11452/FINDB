"""
Django settings for namoro project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!e2v&p^4(-mpumn5o16ieg&!hzisi^2!$2rr#j_2fl(us(w-c^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

""" CSRF_TRUSTED_ORIGINS = [
    'https://3486-187-21-8-3.ngrok-free.app', 
] """

DOMINIO = 'http://127.0.0.1:8000'

from decouple import config

# Stripe
KEY_PUBLIC_STRIPE = config('KEY_PUBLIC_STRIPE')
KEY_SECRET_STRIPE = config('KEY_SECRET_STRIPE')

# E-mail
DEFAULT_FROM_EMAIL=config('EMAIL_HOST_USER')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Zoom
ACCOUNT_ID_ZOOM = config('ACCOUNT_ID_ZOOM')
CLIENT_ID_ZOOM = config('CLIENT_ID_ZOOM')
CLIENT_SECRET_ZOOM = config('CLIENT_SECRET_ZOOM')

# ZEGOCLOUD
ZEGOCLOUD_VIDEO_API_KEY = config('ZEGOCLOUD_VIDEO_API_KEY')
ZEGOCLOUD_VIDEO_SERVER_SECRET = config('ZEGOCLOUD_VIDEO_SERVER_SECRET')
ZEGOCLOUD_AUDIO_API_KEY = config('ZEGOCLOUD_AUDIO_API_KEY')
ZEGOCLOUD_AUDIO_SERVER_SECRET = config('ZEGOCLOUD_AUDIO_SERVER_SECRET')

# Cloudfare
ACCOUNT_ID_CLOUDFARE_R2 = config('ACCOUNT_ID_CLOUDFARE_R2')
TOKEN_API_CLOUDFARE_R2 = config('TOKEN_API_CLOUDFARE_R2')
ACCESS_KEY_ID_CLOUDFARE_R2 = config('ACCESS_KEY_ID_CLOUDFARE_R2')
SECRET_ACCESS_CLOUDFARE_R2 = config('SECRET_ACCESS_CLOUDFARE_R2')
BUCKET_NAME_PERFIL = config('BUCKET_NAME_PERFIL')
BUCKET_NAME_PROFISSIONAL = config('BUCKET_NAME_PROFISSIONAL')
BUCKET_NAME_DOCUMENTOS = config('BUCKET_NAME_DOCUMENTOS')

# Recaptcha
RECAPTCHA_FRONT = config('RECAPTCHA_FRONT')
RECAPTCHA_BACK = config('RECAPTCHA_BACK')
KEY_WEBHOOK = config('KEY_WEBHOOK')

SESSION_COOKIE_AGE = 60 * 60 * 24 * 1
SESSION_SAVE_EVERY_REQUEST = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home.apps.HomeConfig',
    'perfil.apps.PerfilConfig',
    'eventos.apps.EventosConfig',
    'payment.apps.PaymentConfig',
    'comunication.apps.ComunicationConfig',
    'axes',
]

AXES_FAILURE_LIMIT = 4
import datetime as dt
delta = dt.timedelta(minutes=10)
AXES_COOLOFF_TIME = delta
AXES_RESET_ON_SUCCESS = True
AXES_ENABLE_ACCESS_FAILURE_LOG = True
AXES_LOCK_OUT_AT_FAILURE = True

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'perfil.middleware.LoginAdminMiddleware',
    'perfil.middleware.UpdateLastActivityMiddleware',
]

ROOT_URLCONF = 'namoro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'namoro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = False

# Mensagens:
from django.contrib.messages import constants

MESSAGE_TAGS = {
    constants.ERROR: 'erro',
    constants.SUCCESS: 'sucesso',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'templates/static'
]
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
