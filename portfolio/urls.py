from django.urls import include, path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.static import serve
from portfolio.main.views import S3DocumentServe
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls
from django_cas_ng import views as cas_views


admin.autodiscover()


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    path('admin/', admin.site.urls),
    path('stats/', TemplateView.as_view(template_name="stats.html")),
    path('smoketest/', include('smoketest.urls')),
    url(r'^_impersonate/', include('impersonate.urls')),
    re_path(r'^uploads/(?P<path>.*)$',
            serve, {'document_root': settings.MEDIA_ROOT}),
    path('cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/(?P<document_id>\d+)/(.*)$',
            S3DocumentServe.as_view(),
            name='wagtaildocs_serve'),
    path('documents/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
