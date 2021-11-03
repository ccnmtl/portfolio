# Django settings for portfolio project.
import os.path
from ccnmtlsettings.shared import common

project = 'portfolio'
base = os.path.dirname(__file__)

locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'portfolio.main',
]

USE_TZ = True

MIDDLEWARE += [  # noqa
    'django_cas_ng.middleware.CASMiddleware',
    'wagtail.contrib.legacy.sitemiddleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

INSTALLED_APPS += [  # noqa
    'bootstrap4',
    'infranil',
    'django_extensions',
    'django_cas_ng',

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
    'wagtail.core',
    'modelcluster',
    'taggit',

    'portfolio.main',
    'portfolio.featured'
]

INSTALLED_APPS.remove('djangowind') # noqa

THUMBNAIL_SUBDIR = "thumbs"
LOGIN_REDIRECT_URL = "/"

WAGTAIL_SITE_NAME = 'CTL Portfolio'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend'
]

CAS_SERVER_URL = 'https://cas.columbia.edu/cas/'
CAS_VERSION = '3'
CAS_ADMIN_REDIRECT = False

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
