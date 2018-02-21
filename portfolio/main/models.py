from __future__ import unicode_literals

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from modelcluster.fields import ParentalManyToManyField

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


@register_snippet
class Partner(Orderable):

    name = models.CharField(max_length=255)
    short_title = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('short_title'),
        FieldPanel('affiliation'),
    ]


@register_snippet
class Discipline(Orderable):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
    ]


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def entries(self):
        # Get list of project Entries
        entries = Entry.objects.live().public()
        # sort here, return only six cards
        entries = entries.order_by('-release_date')[:6]

        return entries

    def featured_entries(self):
        # Get list of featured project Entries
        featured_entries = Entry.objects.live().public().filter(
            feature_on_homepage=True)
        # sort here, return only 3 cards
        featured_entries = featured_entries.order_by('-last_published_at')[:3]

        return featured_entries


class VisualIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    parent_page_types = ['HomePage']
    subpage_types = ['Entry']

    def get_context(self, request):
        context = super(VisualIndex, self).get_context(request)

        sort_order = self.get_sort(request)
        entries = Entry.objects.live().public().order_by(sort_order)

        # Pagination
        per_page = 6
        page = request.GET.get('page')
        paginator = Paginator(entries, per_page)
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        context['sort'] = request.GET.get('sort', 'releasedate')
        context['entries'] = entries
        return context

    def get_sort(self, request):
        if request.GET.get('sort', 'releasedate') == 'releasedate':
            return '-release_date'
        else:
            return 'title'


class TextualIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = []

    def entries(self):
        # Get list of project Entries
        entries = Entry.objects.live().public().order_by('title')
        # sort here if desired
        return entries


class StaticPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]

    subpage_types = []


class Entry(Page, TimeStampedModel):

    discipline = ParentalManyToManyField(
        Discipline,
        help_text='Which discipline is this project for?',
        blank=True)
    overview = models.CharField(
        help_text='A blurb highlighting the project\'s purpose and effort. '
        'Think of it as an elevator pitch',
        max_length=255, blank=True)
    description = RichTextField(
        help_text='The main content of this Portfolio entry page', blank=True)
    project_url = models.URLField(
        help_text='URL of this project, if available.', blank=True)
    release_date = models.DateField(
        help_text='Format YYYY-MM-DD')
    partners = ParentalManyToManyField(Partner, blank=True)
    feature_on_homepage = models.BooleanField(default=False)
    feature_blurb = models.CharField(
        help_text='A very short blurb on this entry for the feature carousel',
        max_length=255, blank=True)
    poster = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension 1140px by 555px. Format: PNG or JPG.'
    )
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension 600px by 315px. Format: PNG or JPG.'
    )
    infosheet = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='PDF information sheet for printing, if available.'
    )

    parent_page_types = ['VisualIndex']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('overview'),
        FieldPanel('description', classname="full"),
        FieldPanel('release_date'),
        FieldPanel('discipline', widget=forms.SelectMultiple),
        FieldPanel('partners', widget=forms.SelectMultiple),
        FieldPanel('project_url'),
        MultiFieldPanel(
            [
                ImageChooserPanel('poster'),
                ImageChooserPanel('thumbnail'),
            ],
            heading="Representational images"
        ),
        DocumentChooserPanel('infosheet'),
        MultiFieldPanel(
            [
                FieldPanel('feature_on_homepage'),
                FieldPanel('feature_blurb'),
            ],
            heading="Homepage Feature Carousel"
        ),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]
