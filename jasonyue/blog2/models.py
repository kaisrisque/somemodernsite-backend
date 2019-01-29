from django.db import models
from django.utils import timezone
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.api import APIField
from wagtail.api.v2.endpoints import BaseAPIEndpoint

# Keep the definition of BlogIndexPage, and add:


class BlogPage(Page):
    published_date = models.DateField(default=timezone.now)
    intro = models.CharField(max_length=250)
    text = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('text'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('published_date'),
        FieldPanel('intro'),
        FieldPanel('text', classname="full"),
    ]

    # Export fields over the API
    api_fields = [
        APIField('published_date'),
        APIField('intro'),
        APIField('text'),
    ]