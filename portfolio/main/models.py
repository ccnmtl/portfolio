from __future__ import unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class Entry(Page):

    nut_graph = models.CharField(max_length=180, blank=True)
    body = RichTextField(blank=True)
    site_url = models.URLField(blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('nut_graph'),
        FieldPanel('body', classname="full"),
        FieldPanel('site_url'),
    ]