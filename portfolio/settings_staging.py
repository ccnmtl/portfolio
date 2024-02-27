from portfolio.settings_shared import *  # noqa: F403
from ctlsettings.staging import common

BASE_URL = 'https://portfolio.stage.ctl.columbia.edu'

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
