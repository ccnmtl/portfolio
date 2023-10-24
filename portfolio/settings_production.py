from django.conf import settings
from portfolio.settings_shared import *  # noqa: F403
from ctlsettings.production import common
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_URL = 'https://portfolio.ctl.columbia.edu'

locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        s3prefix='ccnmtl',
    ))

try:
    from portfolio.local_settings import *  # noqa: F403
except ImportError:
    pass

if hasattr(settings, 'SENTRY_DSN'):
    sentry_sdk.init(
        dsn=SENTRY_DSN,  # noqa: F405
        integrations=[DjangoIntegration()],
    )
