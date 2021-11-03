from django.test import TestCase
from django.test.client import RequestFactory

from portfolio.featured.views import FeaturedView
from portfolio.main.models import Entry
from portfolio.main.tests.factories import EntryFactory


class FeaturedViewTest(TestCase):

    def test_initialize_slots(self):
        EntryFactory(path='0002', feature_on_homepage=False)
        e1 = EntryFactory(path='0003',
                          feature_on_homepage=True, feature_slot=1)
        e2 = EntryFactory(path='0004',
                          feature_on_homepage=True, feature_slot=0)

        view = FeaturedView()
        slots = view.initialize_slots()

        self.assertEqual(slots[0], e2)
        self.assertEqual(slots[1], e1)

    def test_set_featured_valid(self):
        self.assertEqual(
            Entry.objects.filter(feature_on_homepage=True).count(), 0)

        e = EntryFactory(path='0002', feature_on_homepage=False)

        view = FeaturedView()

        data = {
            'feature-entry-1': e.id,
            'feature-blurb-1': 'A very cool project'
        }
        view.request = RequestFactory().post('/', data)
        view.set_featured('feature-entry-1')

        e.refresh_from_db()
        self.assertTrue(e.feature_on_homepage)
        self.assertEqual(e.feature_slot, 0)
        self.assertEqual(e.feature_blurb, 'A very cool project')

        self.assertEqual(
            Entry.objects.filter(feature_on_homepage=True).count(), 1)

    def test_set_featured_invalid(self):
        view = FeaturedView()

        data = {
            'feature-entry-1': 789,
            'feature-blurb-1': 'A very cool project'
        }
        view.request = RequestFactory().post('/', data)
        view.set_featured('feature-entry-1')

        self.assertEqual(
            Entry.objects.filter(feature_on_homepage=True).count(), 0)

    def test_post(self):

        e1 = EntryFactory(path='0003', feature_on_homepage=False)
        e2 = EntryFactory(path='0004', feature_on_homepage=True,
                          feature_slot=1, feature_blurb='e2 blurb')
        e3 = EntryFactory(path='0005', feature_on_homepage=True,
                          feature_slot=0, feature_blurb='e3 change me')

        self.assertEqual(
            Entry.objects.filter(feature_on_homepage=True).count(), 2)

        data = {
            'feature-entry-1': e1.id,
            'feature-blurb-1': 'e1 blurb',
            'feature-entry-2': e3.id,
            'feature-blurb-2': 'e3 blurb'
        }
        view = FeaturedView()
        view.request = RequestFactory().post('/', data)

        view.post()
        e1.refresh_from_db()
        e2.refresh_from_db()
        e3.refresh_from_db()

        self.assertEqual(
            Entry.objects.filter(feature_on_homepage=True).count(), 2)

        self.assertTrue(e1.feature_on_homepage)
        self.assertEqual(e1.feature_blurb, 'e1 blurb')
        self.assertEqual(e1.feature_slot, 0)

        self.assertFalse(e2.feature_on_homepage)
        self.assertEqual(e2.feature_blurb, None)
        self.assertEqual(e2.feature_slot, None)

        self.assertTrue(e3.feature_on_homepage)
        self.assertEqual(e3.feature_blurb, 'e3 blurb')
