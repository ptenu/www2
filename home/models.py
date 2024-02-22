from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

from guidance.models import GuidanceTopic
from news.models import NewsPost


class HomePage(Page):

    def get_topics(self):
        return GuidanceTopic.objects.live().order_by("title")

    def get_news(self):
        return NewsPost.objects.live().order_by("-created_at")[:3]


class ContentPage(Page):
    body = RichTextField(blank=True)
    show_siblings = models.BooleanField(blank=False, default=False)

    content_panels = Page.content_panels + [FieldPanel("body")]

    settings_panels = Page.settings_panels + [FieldPanel("show_siblings")]
