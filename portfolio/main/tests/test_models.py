from django.test import TestCase
from portfolio.main.tests.factories import EntryFactory
from portfolio.main.models import HomePage, VisualIndex
from django.test.client import RequestFactory


class TestHomePage(TestCase):
    def test_entries(self):
        EntryFactory(live=False, path='0002')
        e = EntryFactory(path='0003')
        h = HomePage()
        qs = h.entries()

        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs.first(), e)

    def test_featured_entries(self):
        EntryFactory(feature_on_homepage=False, path='0002')
        e = EntryFactory(feature_on_homepage=True, path='0003')
        h = HomePage()
        qs = h.featured_entries()

        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs.first(), e)


class TestVisualIndex(TestCase):
    def test_get_context(self):
        EntryFactory(live=False, path='0002')
        e = EntryFactory(path='0003')
        v = VisualIndex()
        r = RequestFactory().get('/')

        ctx = v.get_context(r)

        self.assertEquals(ctx['sort'], 'releasedate')
        self.assertEquals(ctx['entries'].object_list.first(), e)
