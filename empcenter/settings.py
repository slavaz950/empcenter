"""
Django settings for empcenter project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.urls import reverse_lazy
from django.core.mail.backends.smtp import EmailBackend

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v8p7m8qq23*8cr(ivlh203$1kjn$niz6gdu$33u3wm!-8qi*0m'

# SECURITY WARNING: don't run with debug turned on in production!
# ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ: не запускайте с включенной отладкой в рабочей среде.
DEBUG = True    # #     True   False 

ALLOWED_HOSTS =  []   #  "http://127.0.0.1:8000/"" #   "192.168.3.45"


"""
# Настройка для отладочного smtp-сервера Джанго
EMAIL_HOST = 'localhost' # Интернет-адрес SMTP-сервера, которому будут отправляться письма ('localhost' по умолчанию)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Строка с именем класса, который реализует отправку писем 
DEFAULT_FROM_EMAIL = "webmaster@localhost"   # Адрес электронной почты отправителя, по умолчанию указываемый
EMAIL_PORT = 1025  # Номер  TCP- порта, через который работает  SMTP-сервер, в виде числа(По умолчанию: 25)


"""

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Строка с именем класса, который реализует отправку писем 
# Настройка smtp-сервера на Яндексе (порт 465 или 587)
EMAIL_HOST = 'smtp.yandex.ru'   # Доменное имя почтового SMTP-сервера Яндекса
EMAIL_PORT = 465   # Порт почтового SMTP-сервера Яндекса. Перед использованием рекомендуется загуглить и проверить его актуальность
EMAIL_USE_TLS = False   # Может работать только один из них. Поэтому
EMAIL_USE_SSL = True     # один False другой True. Всё зависит от настроек (в данном случае Яндекса)

EMAIL_SSL_CERTFILE = None # Если TLS или SSL = True
EMAIL_SSL_KEYFILE = None # Если TLS или SSL = True
EMAIL_TIMEOUT = None # Промежуток времени, в течении которого класс-отправитель будет пытаться установить соединение
#  с SMPT-сервером, в виде целого числа в секундах. Если соединение установить не удаётся, будет возбуждено исключение
# timeout  из модуля  socket. По умролчанию None
EMAIL_USE_LOCALTIME = True # 

EMAIL_HOST_USER = 'empcenter@yandex.ru'  # Логин Яндекса (пишем полностью (Рекомендуется. Но возможно буду работать и другие варианты написания))
EMAIL_HOST_PASSWORD = 'egcvsgrizerdrhpi'   #  Пароль приложения который получили в Яндексе. (В случае забыли(потеряли) в Яндексе удаляем и создаём новый )
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER    
SERVER_EMAIL = EMAIL_HOST_USER 
EMAIL_ADMIN =EMAIL_HOST_USER 


#EMAIL_PORT = 1025  # Порт для отладочного сервера


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'bootstrap4',
    'django_cleanup', # Удаляет выгруженные файлы после удаления хранящих их записей модулей
    'easy_thumbnails', # Создаёт миниатюры
    'captcha',
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

ROOT_URLCONF = 'empcenter.urls'

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
                'main.middlewares.empcenter_context_processor', # Обработчик контекста для рубрик
                
            ],
        },
    },
]

WSGI_APPLICATION = 'empcenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'empcenter.data'),
    }
}

AUTH_USER_MODEL = 'main.AdvUser'

#LOGIN_REDIRECT_URL = reverse_lazy("main:profile")
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

THUMBNALL_ALIASES = {
    '': {
        'default': {
            'size': (96,96),  # Масштабирование для миниатюр
            'crop': 'scale',  # Имя вложенной папки в которой хранятся миниатюры
        },
    },
}


