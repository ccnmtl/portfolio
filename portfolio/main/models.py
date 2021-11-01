from __future__ import unicode_literals

import re

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Partner(Orderable):

    name = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    short_title = models.CharField(
        max_length=255, help_text='e.g. Professor, Librarian, Lecturer')
    full_title = models.TextField(
        blank=True,
        help_text='e.g. Dewitt Clinton Professor Emeritus of History')
    headshot = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension 300px by 300px. Format: PNG or JPG.'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('short_title'),
        FieldPanel('full_title'),
        FieldPanel('affiliation'),
        ImageChooserPanel('headshot')
    ]


@register_snippet
class Discipline(Orderable):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
    ]


@register_snippet
class ProjectType(Orderable):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
    ]


@register_snippet
class AwardType(Orderable):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

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
        entries = Entry.objects.live().public()

        q = request.GET.get('q', '')
        if q:
            entries = entries.filter(title__icontains=q)

        entries = entries.order_by(sort_order)

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
        context['q'] = q
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
        'Think of it as an elevator pitch.',
        max_length=255, blank=True)
    description = RichTextField(
        help_text='The main content of this Portfolio entry page.', blank=True)
    project_url = models.URLField(
        help_text='URL of this project\'s home page.', blank=True)
    release_date = models.DateField(help_text='Format YYYY-MM-DD')
    revision_date = models.DateField(
        blank=True, null=True,
        help_text='Format YYYY-MM-DD. '
        'This applies only to a project revision, a MOOC relaunch, '
        'or an institute rerun.')
    partners = ParentalManyToManyField(Partner, blank=True)
    project_type = ParentalManyToManyField(ProjectType, blank=True)
    award_type = ParentalManyToManyField(AwardType, blank=True)
    feature_on_homepage = models.BooleanField(default=False)
    feature_blurb = models.CharField(
        help_text='A very short blurb on this entry for the feature carousel.',
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
        help_text='PDF information sheet for printing.'
    )

    video_url = models.URLField(
        help_text='URL of the promotional video.', blank=True)
    video_title = models.CharField(max_length=255, blank=True)

    gallery_image_one = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension 300px by 300px. Format: PNG or JPG.'
    )
    gallery_image_two = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension 300px by 300px. Format: PNG or JPG.'
    )
    gallery_image_three = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension 300px by 300px. Format: PNG or JPG.'
    )

    parent_page_types = ['VisualIndex']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('overview'),
        FieldPanel('description', classname="full"),
        FieldPanel('release_date'),
        FieldPanel('revision_date'),
        FieldPanel('partners', widget=forms.SelectMultiple),
        FieldPanel('project_type'),
        FieldPanel('award_type'),
        FieldPanel('discipline', widget=forms.SelectMultiple),
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
        MultiFieldPanel(
            [
                FieldPanel('video_title'),
                FieldPanel('video_url')
            ],
            heading='Promotional Video'
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('gallery_image_one'),
                ImageChooserPanel('gallery_image_two'),
                ImageChooserPanel('gallery_image_three'),
            ],
            heading='Image Gallery'
        )
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]

    def full_clean(self, *args, **kwargs):
        if not self.revision_date:
            self.revision_date = self.release_date
        super().full_clean(*args, **kwargs)

    def youtube_video_url(self):
        """
        A utility function to ease confusion around the youtube embed url.

        If the video_url is ...
        : in the youtube embed format, return as is
        : in the youtube watch format, return the youtube embed format
        : otherwise, return None

        More tests may be needed in the future.
        """

        if re.search(r'www.youtube.com\/embed', self.video_url):
            return self.video_url

        vid = re.search(r'www.youtube.com\/watch\?v=(.*)', self.video_url)
        if vid:
            return 'https://www.youtube.com/embed/{}'.format(vid.group(1))

        return None
