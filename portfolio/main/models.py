from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel


class Entry(Page):

    overview = models.CharField(max_length=255, blank=True)
    body = RichTextField(
        help_text='The main content of this Portfolio entry page', blank=True)
    project_url = models.URLField(
        help_text='URL of this project', blank=True)
    release_date = models.DateField(
        help_text='Format YYYY-MM-DD')
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
        FieldPanel('body', classname="full"),
        FieldPanel('release_date'),
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
