# sitemaps.py
from django.contrib import sitemaps

from portfolio.main.models import Entry


class StaticPageSitemap(sitemaps.Sitemap):

    changefreq = 'weekly'

    def items(self):
        return ['main', 'about']

    def location(self, item):
        if item == 'main':
            return '/'
        elif item == 'about':
            return '/about/'


class EntrySitemap(sitemaps.Sitemap):

    changefreq = 'weekly'

    def items(self):
        return list(Entry.objects.live())

    def location(self, item):
        return item.get_absolute_url()
