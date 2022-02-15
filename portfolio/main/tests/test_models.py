from django.test import TestCase
from django.test.client import RequestFactory
from portfolio.main.models import HomePage, VisualIndex
from portfolio.main.tests.factories import EntryFactory, PartnerFactory


class HomePageTest(TestCase):
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


class VisualIndexTest(TestCase):

    def test_get_context(self):
        EntryFactory(live=False, path='0002')
        e = EntryFactory(path='0003')
        v = VisualIndex()
        r = RequestFactory().get('/')

        ctx = v.get_context(r)

        self.assertEquals(ctx['sort'], 'releasedate')
        self.assertEquals(ctx['entries'].object_list.first(), e)

    def test_get_context_search(self):
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004')

        v = VisualIndex()
        r = RequestFactory().get('/?q=foo')

        ctx = v.get_context(r)

        self.assertEquals(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['q'], 'foo')
        self.assertEquals(ctx['entries'].object_list.count(), 1)
        self.assertEquals(ctx['entries'].object_list.first(), e3)

    def test_get_context_search_partner(self):
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004')
        e3.partners.get_original_manager().add(PartnerFactory())
        self.assertEqual(e3.partners.first().name, 'James Moriarty')

        v = VisualIndex()
        r = RequestFactory().get('/?q=moriarty')

        ctx = v.get_context(r)

        self.assertEquals(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['q'], 'moriarty')
        self.assertEquals(ctx['entries'].object_list.count(), 1)
        self.assertEquals(ctx['entries'].object_list.first(), e3)

    def test_get_context_search_description(self):
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004', description='baz')

        v = VisualIndex()
        r = RequestFactory().get('/?q=baz')

        ctx = v.get_context(r)

        self.assertEquals(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['q'], 'baz')
        self.assertEquals(ctx['entries'].object_list.count(), 1)
        self.assertEquals(ctx['entries'].object_list.first(), e3)


class EntryPageTest(TestCase):

    def test_youtube_video_url(self):
        entry = EntryFactory(
            live=False, path='0002', video_url='https://vimeo.com')
        self.assertIsNone(entry.youtube_video_url())

        entry.video_url = 'https://www.youtube.com/watch?v=2qJPxzgPlzQ'
        self.assertEqual(entry.youtube_video_url(),
                         'https://www.youtube.com/embed/2qJPxzgPlzQ')

        entry.video_url = 'https://www.youtube.com/embed/2qJPxzgPlzQ'
        self.assertEqual(entry.youtube_video_url(),
                         'https://www.youtube.com/embed/2qJPxzgPlzQ')
