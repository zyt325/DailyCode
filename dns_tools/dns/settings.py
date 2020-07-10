"""
Django settings for dns project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gz2m1!-r85yt@#kb5l0raj6^nc23bc=900vav#9y9kdb-&ukht'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['0.0.0.0']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sites',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

ROOT_URLCONF = 'dns.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'sites/templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'jinja2_env.environment',
        },
    },
]

WSGI_APPLICATION = 'dns.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
LOCALHOST = True
if DEBUG and LOCALHOST:
    db_host = 'db08.base-fx.com'
    db_port = 3306
    db_user = 'root'
    db_pass = 'basefx12'
elif not DEBUG:
    db_host = '127.0.0.1'
    db_port = 3306
    db_user = 'root'
    db_pass = ''
else:
    db_host = '127.0.0.1'
    db_port = 3306
    db_user = 'root'
    db_pass = 'mysql325'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'host': 'docker03.base-fx.com',
            'port': 3306,
            'user': 'root',
            'password': 'mysql325',
            'charset': 'utf8mb4',
            'database': 'dns_django',
            'sql_mode': 'STRICT_ALL_TABLES',
        }
    },
    'dns': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'host': db_host,
            'port': db_port,
            'user': db_user,
            'password': db_pass,
            'charset': 'utf8',
            'database': 'dns',
            'sql_mode': 'STRICT_ALL_TABLES',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = os.path.join(BASE_DIR, 'sites/static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'sites/static'),
# ]

