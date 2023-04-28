from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from portfolio.featured.views import FeaturedView


@hooks.register('register_admin_urls')
def register_featured_url():
    return [
        path('featured/', FeaturedView.as_view(), name='featured'),
    ]


@hooks.register('register_admin_menu_item')
def register_calendar_menu_item():
    return MenuItem('Featured', reverse('featured'), icon_name='pick')
