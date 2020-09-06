
import os

from .settings import *
# from .email_info import *




DEBUG = False


assert SECRET_KEY is not None, (
    'Please provide DJANGO_SECRET_KEY'
    'environment variable with a value')


ALLOWED_HOSTS += [
    os.getenv('DJANGO_ALLOWED_HOSTS'),
]


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES['default'].update({
    'NAME': os.getenv('DJANGO_DB_NAME'),
    'USER': os.getenv('DJANGO_DB_USER'),
    'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
    'HOST': os.getenv('DJANGO_DB_HOST'),
    'PORT': os.getenv('DJANGO_DB_PORT'),
})


# Email Config

# EMAIL_HOST = EMAIL_HOST
# EMAIL_PORT = EMAIL_PORT
# EMAIL_HOST_USER = EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_USE_TLS = EMAIL_USE_TLS
# EMAIL_USE_SSL = EMAIL_USE_SSL

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# this will go to console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# If a secure connection is required or not
# EMAIL_USE_TLS

# PASSWORD_RESET_TIMEOUT_DAYS = 2