import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/portfolio/portfolio/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/portfolio/portfolio/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio.settings_staging'

import django
django.setup()

import django.core.wsgi import get_wsgi_application
application = get_wsgi_application()