from datetime import datetime

from django.core.management.base import (
    BaseCommand, CommandError
)
from wagtail.core.models import Page, Site

from portfolio.main.models import (
    HomePage, VisualIndex, TextualIndex, Entry)
from portfolio.main.tests.factories import (
    AwardTypeFactory, DisciplineFactory, ProjectTypeFactory)


def add_entry(parent, title, featured):
    entry = Entry(title=title)
    entry.overview = \
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    entry.description = \
        'Duis maximus nisi lorem, vel commodo nisi imperdiet in.'
    entry.release_date = datetime.now()
    entry.revision_date = datetime.now()
    entry.project_url = 'https://ctl.columbia.edu'

    parent.add_child(instance=entry)
    entry.save_revision().publish()

    entry.discipline.add(DisciplineFactory())
    entry.project_type.add(ProjectTypeFactory())
    entry.award_type.add(AwardTypeFactory())

    if featured > 0:
        entry.feature_on_homepage = True
        entry.feature_slot = featured
        entry.feature_blurb = ''
        entry.save()


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
        add_entry(our_work, 'From Bystander to Upstander', 1)
        add_entry(our_work, 'Footprints', 2)
        add_entry(our_work, 'Logic Learner', 3)
        add_entry(our_work, 'Locus Tempus', 0)
