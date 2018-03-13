from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
import os.path
from portfolio.main.views import S3DocumentServe
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))
logout_page = url(
    r'^accounts/logout/$',
    logout,
    {'next_page': redirect_after_logout})
if hasattr(settings, 'CAS_BASE'):
    from djangowind.views import logout as windlogout
    auth_urls = url(r'^accounts/', include('djangowind.urls'))
    logout_page = url(
        r'^accounts/logout/$',
        windlogout,
        {'next_page': redirect_after_logout})

urlpatterns = [
    auth_urls,
    logout_page,
    url(r'^admin/', include(admin.site.urls)),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'infranil/', include('infranil.urls')),
    url(r'^uploads/(?P<path>.*)$',
        serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/(?P<document_id>\d+)/(.*)$', S3DocumentServe.as_view(),
        name='wagtaildocs_serve'),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
