from __future__ import unicode_literals

from django import forms
from django.db import models

from django_extensions.db.models import TimeStampedModel

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from modelcluster.fields import ParentalManyToManyField


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

    overview = models.CharField(max_length=255, blank=True)
    description = RichTextField(
        help_text='The main content of this Portfolio entry page', blank=True)
    project_url = models.URLField(
        help_text='URL of this project', blank=True)
    release_date = models.DateField(
        help_text='Format YYYY-MM-DD')
    partners = ParentalManyToManyField(Partner, blank=True)
    infosheet = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        help_text='help me',
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('overview'),
        FieldPanel('description', classname="full"),
        FieldPanel('release_date'),
        FieldPanel('partners', widget=forms.SelectMultiple),
        DocumentChooserPanel('infosheet'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        MultiFieldPanel(
            [
                FieldPanel('project_url'),
            ]
        ),
    ]
