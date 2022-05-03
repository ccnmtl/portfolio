from datetime import datetime

from django.core.management.base import (
    BaseCommand, CommandError
)
from wagtail.core.models import Page, Site
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file

from portfolio.main.models import (
    HomePage, VisualIndex, TextualIndex, Entry, OrderedPartnerSnippet)
from portfolio.main.tests.factories import (
    AwardTypeFactory, DisciplineFactory, ProjectTypeFactory, PartnerFactory)


def add_default_entry(parent, title):
    entry = Entry(title=title)
    entry.overview = \
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    entry.description = \
        'Duis maximus nisi lorem, vel commodo nisi imperdiet in.'
    entry.release_date = datetime.now()

    parent.add_child(instance=entry)
    entry.save_revision().publish()

    OrderedPartnerSnippet.objects.create(page=entry, partner=PartnerFactory())


def add_entry(parent, title, featured):
    entry = Entry(title=title)
    entry.overview = \
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    entry.description = \
        'Duis maximus nisi lorem, vel commodo nisi imperdiet in.'
    entry.release_date = datetime.now()
    entry.revision_date = datetime.now()
    entry.project_url = 'https://ctl.columbia.edu'

    entry.thumbnail = Image.objects.create(
        title='thumbnail',
        file=get_test_image_file(),
    )

    entry.poster = Image.objects.create(
        title='poster',
        file=get_test_image_file(),
    )

    if featured > 0:
        entry.feature_on_homepage = True
        entry.feature_slot = featured
        entry.feature_blurb = ''

    parent.add_child(instance=entry)
    entry.save_revision().publish()

    entry.discipline.add(DisciplineFactory())
    entry.project_type.add(ProjectTypeFactory())
    entry.award_type.add(AwardTypeFactory())

    partner = PartnerFactory()
    partner.headshot = Image.objects.create(
        title='headshot',
        file=get_test_image_file(),
    )
    partner.save()
    OrderedPartnerSnippet.objects.create(page=entry, partner=partner)


class Command(BaseCommand):

    """Build out the basic site tree"""
    def handle(self, *args, **options):
        if Page.objects.count() > 2:
            raise CommandError('There already exists content in the database.')

        # Delete the existing 'Welcome to Wagtail' page, create homepage
        Page.objects.get(id=2).delete()
        Site.objects.all().delete()

        root = Page.objects.get(id=1)
        homepage = HomePage(title='Home')
        root.add_child(instance=homepage)
        homepage.save_revision().publish()

        Site.objects.create(
            hostname='localhost',
            root_page_id=homepage.id,
            is_default_site=True
        )

        our_work = VisualIndex(title='Our Work')
        homepage.add_child(instance=our_work)
        our_work.save_revision().publish()

        textual_index = TextualIndex(
            title='Textual Index', slug='index-listing')
        homepage.add_child(instance=textual_index)
        textual_index.save_revision().publish()

        # Add three entries
        add_entry(our_work, 'Entry One', 1)
        add_entry(our_work, 'Entry Two', 2)
        add_entry(our_work, 'Entry Three', 3)
        add_default_entry(our_work, 'Default Entry')
