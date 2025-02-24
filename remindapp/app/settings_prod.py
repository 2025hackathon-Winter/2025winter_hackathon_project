import os
from pathlib import Path
from datetime import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ya+ni7vkxb$9a*z+w$^arnlmuid6*3vkt0$521^w!e0=2!ljdk'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False
ALLOWED_HOSTS = ["wasurenu-alb-1435726864.ap-northeast-1.elb.amazonaws.com","localhost","127.0.0.1","wasurenu.net"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'remind.apps.RemindConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'remind.middleware.LoggingMiddleware'
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / './templates'], #base_dir間違っているので修正
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'db',
        'PORT': '3306',
        'NAME': 'shopping_remind_app',
        'USER': 'testuser',
        'PASSWORD': 'testpass',
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

today = datetime.today().strftime('%Y-%m-%d')

LOGGING = {
    # ロギング設定のバージョン
    "version": 1,
    #　Django のデフォルトログ（既存のロガー）を無効にするか
    "disable_existing_loggers": False,
    #　ログの出力フォーマットを指定
    # {levelname}:ログのレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    # {asctime}:ログが記録された時間
    # {module}:ログを出力したモジュール名
    # {message}:実際のログメッセージ
    # ↓の書き方での実際の出力　[INFO] 2025-02-23 14:30:00 views サーバーが起動しました
    # styleはこのformatの書き方のスタイルを指定している。
    # verboseは詳細のログ、simpleはシンプルなログ
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",  # WARNING 以上のログを記録
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": f"/var/log/django/app_logs/django_{today}.log",
            "when": "midnight",  # 毎日0時にログをローテーション
            "interval": 1,
            "backupCount": 7,  # 7日分のログを保持
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },

    },
    # propagete:親のロガーに伝わるか？伝える＝True
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.server": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.template": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "WARNING" ,
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file"],
            "level": "WARNING" ,
            "propagate": False,
        },
        "remind": {  # カスタムアプリのログ
            "handlers": ["file","console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja' # アナザーにより変更(2/8)

TIME_ZONE = 'Asia/Tokyo' # アナザーにより変更(2/8)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),] #修正
##For product invironment
STATIC_ROOT = "/var/www/django/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/menu/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

AUTH_USER_MODEL = "remind.CustomUsers"  