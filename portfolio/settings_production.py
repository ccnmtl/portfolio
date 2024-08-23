from django.conf import settings
from ctlsettings.production import common, init_sentry
from portfolio.settings_shared import *  # noqa: F403

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
    from portfolio.local_settings import *  # noqa: F403 F401
except ImportError:
    pass


if hasattr(settings, 'SENTRY_DSN'):
    init_sentry(SENTRY_DSN)  # noqa F405
