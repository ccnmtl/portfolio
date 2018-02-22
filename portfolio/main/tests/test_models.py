from django.test import TestCase
from portfolio.main.tests.factories import EntryFactory
from portfolio.main.models import HomePage


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
