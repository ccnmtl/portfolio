# flake8: noqa
from portfolio.settings_shared import *

try:
    from local_settings import *
except ImportError:
    pass
