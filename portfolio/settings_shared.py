# Django settings for portfolio project.
import os.path
import sys
from ctlsettings.shared import common

project = 'portfolio'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'portfolio.main',
]

USE_TZ = True

MIDDLEWARE += [  # noqa
    'wagtail.contrib.legacy.sitemiddleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

INSTALLED_APPS += [  # noqa
    'bootstrap4',
    'django_extensions',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.api.v2',
    'modelcluster',
    'taggit',
    'django.contrib.sitemaps',

    'portfolio.main',
    'portfolio.featured',
    'waffle'
]

THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

WAGTAIL_SITE_NAME = 'CTL Portfolio'
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 2 * 1024 * 1024   # 2mb
WAGTAILADMIN_BASE_URL = 'https://portfolio.ctl.columbia.edu'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(base, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'stagingcontext.staging_processor',
                'gacontext.ga_processor',
            ],
        },
    },
]

if 'integrationserver' in sys.argv:
    MEDIA_ROOT = './uploads/'
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
            'ATOMIC_REQUESTS': True,
        }
    }
