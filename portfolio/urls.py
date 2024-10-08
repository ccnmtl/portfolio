from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from django_cas_ng import views as cas_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from .api import api_router
from portfolio.main.views import S3DocumentServe
from portfolio.sitemaps import EntrySitemap, StaticPageSitemap


admin.autodiscover()

sitemaps = {
    'static': StaticPageSitemap,
    'entry': EntrySitemap
}

urlpatterns = [
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    path('admin/', admin.site.urls),
    path('stats/', TemplateView.as_view(template_name="stats.html")),
    path('smoketest/', include('smoketest.urls')),
    re_path(r'^_impersonate/', include('impersonate.urls')),
    re_path(r'^uploads/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT}),
    path('cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/(?P<document_id>\d+)/(.*)$',
            S3DocumentServe.as_view(),
            name='wagtaildocs_serve'),
    path('documents/', include(wagtaildocs_urls)),

    path('api/v2/', api_router.urls),
    # Ensure that the api_router line appears above the
    # default Wagtail page serving route
    re_path(r'^', include(wagtail_urls)),

    path('', include(wagtail_urls)),

    path('sitemap.xml', sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
