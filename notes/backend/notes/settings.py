"""
Django settings for notes project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+(mhq$_w!@&(qbqq9@i@=!u4pi9c&^!^0zh!k63)br%a1abt9m'

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
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_jwt',
    'dj_rest_auth',
    'django_filters',
    'note',
    'api',
    'tools',
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

ROOT_URLCONF = 'notes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'apps/tools/templates'),
                 os.path.join(BASE_DIR, 'apps/picm/templates')],
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

WSGI_APPLICATION = 'notes.wsgi.application'

# REST_FRAMEWORK = {
#     '
# }

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,   #可选可不选，如果在此处填写，则优先级大于自定义里面的page
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    # jwt
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
import datetime

JWT_AUTH = {
    # 指明token的有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 是否允许tokern刷新
    'JWT_ALLOW_REFRESH': True,
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASE_APPS_MAPPING = {
    # 'app_name':'database_name'
    'admin': 'default',
    'auth': 'default',
    'authtoken': 'default',
    'contenttypes': 'default',
    'sessions': 'default',
    'note': 'notes',
    'api': 'notes',
    'tools': 'tools',
}

db_host = '10.14.6.159'
# db_host='note.personer.tech'
# db_host = '127.0.0.1'
if DEBUG:
    db_host = db_host
    db_port = 3306
    db_user = 'root'
    db_pass = 'mysql325'
else:
    db_host = db_host
    db_port = 3306
    db_user = 'root'
    db_pass = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'host': db_host,
            'port': db_port,
            'user': db_user,
            'password': db_pass,
            'charset': 'utf8mb4',
            'database': 'notes_django',
            'sql_mode': 'STRICT_ALL_TABLES',
        }
    },
    'notes': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'host': db_host,
            'port': db_port,
            'user': db_user,
            'password': db_pass,
            'charset': 'utf8mb4',
            'database': 'notes',
            'sql_mode': 'STRICT_ALL_TABLES',
        }
    },
    'tools': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'host': db_host,
            'port': db_port,
            'user': db_user,
            'password': db_pass,
            'charset': 'utf8mb4',
            'database': 'tools',
            'sql_mode': 'STRICT_ALL_TABLES',
        }
    }
}

DATABASE_ROUTERS = ['notes.database_router.DatabaseAppsRouter']

# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend','LdapBackend.LDAPBackend']

if not DEBUG:
    LOGGING_CONF = None
    from .Logger import LOGGING

    LOGGING = LOGGING

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

LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# uploads    path:  MEDIA_ROOT/uploads
# article    path:  MEDIA_ROOT/articles

LOGIN_URL = '/login'
