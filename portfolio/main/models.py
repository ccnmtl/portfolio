from __future__ import unicode_literals

from django import forms
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


class Entry(Page, TimeStampedModel):

    affiliation = models.CharField(
        help_text='What department is this project for?',
        max_length=255, blank=True)
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
    poster = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Dimension 1110px by 540px. Format: PNG or JPG.'
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

    content_panels = Page.content_panels + [
        FieldPanel('overview'),
        FieldPanel('description', classname="full"),
        FieldPanel('release_date'),
        FieldPanel('affiliation'),
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
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]
