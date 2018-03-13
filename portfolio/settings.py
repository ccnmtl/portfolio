# flake8: noqa
from portfolio.settings_shared import *

try:
    from portfolio.local_settings import *
except ImportError:
    pass
