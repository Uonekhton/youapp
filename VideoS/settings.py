import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v6-o&fvd&-x$+9fqg6n**$nyobj1%brzl!7q2*h^-&lr^oz=@#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'constance',
	'constance.backends.database',
	'bootstrap3',
	'pagination_bootstrap',
	'registration',
	'embed_video',
	'youapp',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'pagination_bootstrap.middleware.PaginationMiddleware'
]

ROOT_URLCONF = 'VideoS.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')]
		,
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				"django.template.context_processors.i18n",
				"django.template.context_processors.media",
				'django.contrib.messages.context_processors.messages',
				'constance.context_processors.config',
			],
		},
	},
]

WSGI_APPLICATION = 'VideoS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'LOCATION': 'unique-snowflake',
	}
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


AUTH_USER_MODEL = 'youapp.User'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join('static')
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
	'D:\\youapp-master\\static\\',
]
MEDIA_URL = '/media/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_PREFIX = 'constance:myproject:'
CONSTANCE_CONFIG = {
	'SITE_NAME': ('YouApp', 'Название сайта ', str),
	'SITE_DICT': ('Продажа видео', 'Краткое описание сайта ', str),
	'ID_WO': ('150101355894', 'Идентификатор магазина в Wallet One', str),
	'PAGINATION_DEFAULT_PAGINATION': (12, 'Количество роликов на стене ', int),
	'INDEX_MOVIE': (12, 'Количество роликов на главной странице', int),
	'MIN_OUT': (10, 'Минимальная сумма вывода ', int),
	'EMAIL_OUT': ('khramtsov.ilya@gmail.com', 'Почта куда отправлять заявки', str),
	'COEFFICIENT': (1.2 , 'Коэффициент умножения', float),
	
}

# Django registration
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
REGISTRATION_AUTO_LOGIN = True

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apps.django'
EMAIL_HOST_PASSWORD = 'qrg7t912'