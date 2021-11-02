import datetime

from django.test import TestCase

from portfolio.main.tests.factories import EntryFactory
from portfolio.main.utils import published_entries_by_date,\
    featured_entries_by_slot


class UtilsTest(TestCase):

    def test_published_entries_by_date(self):
        EntryFactory(live=False, path='0002')
        e1 = EntryFactory(path='0003')
        e2 = EntryFactory(path='0004',
                          release_date=datetime.datetime(2020, 1, 1))

        qs = published_entries_by_date()

        self.assertEquals(qs.count(), 2)
        self.assertEquals(qs[0], e1)
        self.assertEquals(qs[1], e2)

    def test_featured_entries(self):

        EntryFactory(path='0002', feature_on_homepage=False)
        e1 = EntryFactory(path='0003',
                          feature_on_homepage=True, feature_slot=1)
        e2 = EntryFactory(path='0004',
                          feature_on_homepage=True, feature_slot=0)

        qs = featured_entries_by_slot()

        self.assertEquals(qs.count(), 2)
        self.assertEquals(qs[0], e2)
        self.assertEquals(qs[1], e1)
