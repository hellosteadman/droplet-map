from os import path
from settings_local import *
from django.utils.timezone import now
from datetime import date

TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Mark Steadman', 'marksteadman@me.com'),
)

MANAGERS = ADMINS
TIME_ZONE = None
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True
SITE_ROOT = path.abspath(path.dirname(__file__) + '/../')
MEDIA_ROOT = path.join(SITE_ROOT, 'media') + '/'
STATIC_ROOT = path.join(SITE_ROOT, 'static') + '/'
CRON_FLAG_FILE = path.join(SITE_ROOT, 'cron.flag')

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'pdd3HTaIGKEv)463sT43xdhC{6DmLIh7FHkyjunx41PdjAcQmOGwEE'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.cache.UpdateCacheMiddleware',
	'bambu.sites.middleware.DomainRedirectMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'bambu.analytics.middleware.AnalyticsMiddleware',
	'bambu.enqueue.middleware.EnqueueMiddleware',
	'django.middleware.cache.FetchFromCacheMiddleware',
)

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = ''

ROOT_URLCONF = 'droplet.urls'

TEMPLATE_DIRS = (
	path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.tz',
	'bambu.bootstrap.context_processors.basics',
	'droplet.stream.context_processors.charts',
	'droplet.stream.context_processors.locations',
	'droplet.context_processors.basics'
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	'django.contrib.markup',
	'django.contrib.humanize',
	'django.contrib.sitemaps',
	'raven.contrib.django.raven_compat',
	'south',
	'sorl.thumbnail',
	'bambu.analytics',
	'bambu.cron',
	'bambu.bootstrap.v2',
	'bambu.mapping',
	'bambu.attachments',
	'bambu.pages',
	'bambu.enqueue',
	'droplet.stream'
)

BOOTSTRAP_CSS_URL = 'css/bootstrap.min.css'

LOGGING = {
	'version': 1,
	'disable_existing_loggers': True,
	'root': {
		'level': 'DEBUG',
		'handlers': ['console']
	},
	'formatters': {
		'verbose': {
			'format': '%(message)s'
		}
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler'
		}
	},
	'loggers': {
		'django.db.backends': {
			'level': 'ERROR',
			'handlers': ['console'],
			'propagate': False
		}
	}
}

MAPPING_PROVIDER = 'bambu.mapping.providers.google.GoogleMapsProvider'
MAPPING_SETTINGS = {
	'api_key': 'AIzaSyCqt9ST-227LGZIt1OmWetj0ORr-Tbn330',
	'zoom': 14,
	'controls': ['PAN', 'ZOOM']
}

THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_DEBUG = False
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'