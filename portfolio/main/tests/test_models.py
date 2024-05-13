from django.test import TestCase
from django.test.client import RequestFactory

from portfolio.main.models import HomePage, VisualIndex, OrderedPartnerSnippet
from portfolio.main.tests.factories import (
    EntryFactory, PartnerFactory, ProjectTypeFactory, AwardTypeFactory)


class HomePageTest(TestCase):
    def test_entries(self):
        EntryFactory(live=False, path='0002')
        e = EntryFactory(path='0003')
        h = HomePage()
        qs = h.entries()

        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), e)

    def test_featured_entries(self):
        EntryFactory(feature_on_homepage=False, path='0002')
        e = EntryFactory(feature_on_homepage=True, path='0003')
        h = HomePage()
        qs = h.featured_entries()

        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), e)


class VisualIndexTest(TestCase):

    def test_get_context(self):
        EntryFactory(live=False, path='0002')
        e = EntryFactory(path='0003')
        v = VisualIndex()
        r = RequestFactory().get('/')

        ctx = v.get_context(r)

        self.assertEqual(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['entries'].object_list.first(), e)

    def test_get_context_search(self):
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004')

        v = VisualIndex()
        r = RequestFactory().get('/?q=foo')

        ctx = v.get_context(r)

        self.assertEqual(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['q'], 'foo')
        self.assertEqual(ctx['entries'].object_list.count(), 1)
        self.assertEqual(ctx['entries'].object_list.first(), e3)

    def test_get_context_search_partner(self):
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004')

        OrderedPartnerSnippet.objects.create(page=e3, partner=PartnerFactory())

        self.assertEqual(e3.ordered_partners.count(), 1)
        self.assertEqual(e3.ordered_partners.all().first().partner.name,
                         'James Moriarty')

        v = VisualIndex()
        r = RequestFactory().get('/?q=moriarty')

        ctx = v.get_context(r)

        self.assertEqual(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['q'], 'moriarty')
        self.assertEqual(ctx['entries'].object_list.count(), 1)
        self.assertEqual(ctx['entries'].object_list.first(), e3)

    def test_get_context_search_description(self):
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004', description='baz')

        v = VisualIndex()
        r = RequestFactory().get('/?q=baz')

        ctx = v.get_context(r)

        self.assertEqual(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['q'], 'baz')
        self.assertEqual(ctx['entries'].object_list.count(), 1)
        self.assertEqual(ctx['entries'].object_list.first(), e3)

    def test_get_context_search_project_type(self):
        pt = ProjectTypeFactory(name='MOOC')
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004', project_type=pt)

        v = VisualIndex()
        r = RequestFactory().get('/?type=mooc')

        ctx = v.get_context(r)

        self.assertEqual(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['type'], 'mooc')
        self.assertEqual(ctx['entries'].object_list.count(), 1)
        self.assertEqual(ctx['entries'].object_list.first(), e3)

    def test_get_context_search_award_type(self):
        award = AwardTypeFactory(name='Innovative Course Design')
        EntryFactory(live=False, path='0002')
        EntryFactory(path='0003')
        e3 = EntryFactory(title='foo', path='0004', award_type=award)

        v = VisualIndex()
        r = RequestFactory().get('/?award=innovative course design')

        ctx = v.get_context(r)

        self.assertEqual(ctx['sort'], 'releasedate')
        self.assertEqual(ctx['award'], 'innovative course design')
        self.assertEqual(ctx['entries'].object_list.count(), 1)
        self.assertEqual(ctx['entries'].object_list.first(), e3)


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
