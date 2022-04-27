from __future__ import unicode_literals

import re

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.db.models.query_utils import Q
from django.utils.html import escape
from django_extensions.db.models import TimeStampedModel
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from portfolio.main.utils import (
    published_entries_by_date, featured_entries_by_slot)
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.admin.edit_handlers import InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Partner(models.Model):

    name = models.CharField(
        max_length=255, help_text='Full name. Example: Eric Foner')
    affiliation = models.CharField(
        max_length=255, help_text='Faculty partner\'s department')
    short_title = models.CharField(
        max_length=255, help_text='Example: Professor, Librarian, Lecturer')
    full_title = models.TextField(
        blank=True,
        help_text='Example: Dewitt Clinton Professor Emeritus of History')
    headshot = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Minimum 300px by 300px. Format: PNG or JPG.'
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


class OrderedPartnerSnippet(Orderable):
    page = ParentalKey('Entry', on_delete=models.CASCADE,
                       related_name='ordered_partners')
    partner = models.ForeignKey(
        'Partner', on_delete=models.CASCADE, related_name='partner')

    panels = [
        SnippetChooserPanel('partner'),
    ]

    class Meta:
        # unique_together = ('page', 'partner')
        # ordering is not automatically inherited from Orderable
        ordering = ['sort_order']


@register_snippet
class Discipline(Orderable):

    name = models.CharField(
        max_length=255, help_text='Example: Literature')

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
        return published_entries_by_date()

    def featured_entries(self):
        return featured_entries_by_slot()


class VisualIndex(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    parent_page_types = ['HomePage']
    subpage_types = ['Entry']

    def filter_by_award_type(self, request, entries):
        award = request.GET.get('award', '')
        award = escape(award)
        if award:
            entries = entries.filter(award_type__name__iexact=award)

        return entries

    def filter_by_project_type(self, request, entries):
        project_type = request.GET.get('type', '')
        project_type = escape(project_type)
        if project_type:
            entries = entries.filter(project_type__name__iexact=project_type)

        return entries

    def get_context(self, request):
        context = super(VisualIndex, self).get_context(request)

        sort_order = self.get_sort(request)
        entries = Entry.objects.live().public()

        q = request.GET.get('q', '')
        q = escape(q)
        if q:
            entries = entries.filter(
                Q(title__icontains=q) | Q(description__icontains=q) |
                Q(ordered_partners__partner__name__icontains=q) |
                Q(project_type__name__iexact=q))

        entries = self.filter_by_project_type(request, entries)
        entries = self.filter_by_award_type(request, entries)
        entries = entries.distinct().order_by(sort_order)

        # Pagination
        per_page = 10
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
        context['type'] = request.GET.get('type', '')
        context['award'] = request.GET.get('award', '')
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
        help_text='Which academic discipline is this project for?',
        blank=True)
    overview = models.CharField(
        help_text='A highlight of the entry\'s purpose and effort, '
        'a tagline, or the main takeaway from the project. '
        'Maximum 255 characters.',
        max_length=255, blank=True)
    description = RichTextField(
        help_text='The main descriptive text of this Portfolio entry page.',
        blank=True)
    project_url = models.URLField(
        help_text='URL for the project or program, at the CTL or elsewhere. '
        'Example: https://mediathread.ctl.columbia.edu', blank=True)
    release_date = models.DateField(
        help_text='Format YYYY-MM-DD. '
        'Date of project first release.')
    revision_date = models.DateField(
        blank=True, null=True,
        help_text='Format YYYY-MM-DD. '
        'This applies only to a project revision, a MOOC relaunch, '
        'or an institute rerun.')
    project_type = ParentalManyToManyField(
        ProjectType, blank=True,
        help_text='SKIP THIS!')
    award_type = ParentalManyToManyField(
        AwardType, blank=True,
        help_text='For project or program that received grants '
        'from the Provost office.')
    feature_on_homepage = models.BooleanField(default=False)
    feature_blurb = models.CharField(
        help_text='A very short blurb on this entry for the feature carousel.',
        max_length=255, null=True, blank=True)
    feature_slot = models.PositiveIntegerField(null=True, blank=True)
    poster = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Minimum 1140px-width by 530px-height. '
        'Format: PNG or JPG.'
    )
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='1200px-width by 630px-height. '
        'Acceptable:  600px width by 315px height. '
        'Format: PNG or JPG.'
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
        help_text='Minimum width 800px. Format: PNG or JPG.'
    )
    gallery_caption_one = models.TextField(blank=True, null=True)

    gallery_image_two = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Minimum width 800px. Format: PNG or JPG.'
    )
    gallery_caption_two = models.TextField(blank=True, null=True)

    gallery_image_three = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Minimum width 800px. Format: PNG or JPG.'
    )
    gallery_caption_three = models.TextField(blank=True, null=True)

    parent_page_types = ['VisualIndex']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('overview'),
        FieldPanel('description', classname="full"),
        FieldPanel('release_date'),
        FieldPanel('revision_date'),
        MultiFieldPanel(
            [
                InlinePanel("ordered_partners", label="Partners")
            ],
            heading="Partners"
        ),
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
                FieldPanel('video_title'),
                FieldPanel('video_url')
            ],
            heading='Promotional Video'
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('gallery_image_one'),
                FieldPanel('gallery_caption_one')
            ],
            heading='First Gallery Image'
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('gallery_image_two'),
                FieldPanel('gallery_caption_two')
            ],
            heading='Second Gallery Image'
        ),
        MultiFieldPanel(
            [
                ImageChooserPanel('gallery_image_three'),
                FieldPanel('gallery_caption_three')
            ],
            heading='Third Gallery Image'
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

        if re.search(r'www\.youtube\.com\/embed', self.video_url):
            return self.video_url

        vid = re.search(r'www\.youtube\.com\/watch\?v=(.*)', self.video_url)
        if vid:
            return 'https://www.youtube.com/embed/{}'.format(vid.group(1))

        return None
