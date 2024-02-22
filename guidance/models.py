from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class GuidanceTopic(Page):
    subtitle = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=False)

    content_panels = Page.content_panels + [FieldPanel("subtitle"), FieldPanel("body")]

    def get_topic_pages(self):
        return self.get_children().live().order_by("title")


class GuidancePage(Page):
    subtitle = models.CharField(max_length=250, blank=True)
    body = RichTextField(blank=False)
    last_reviewed = models.DateField(verbose_name="Last reviewed on")

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("last_reviewed"),
        FieldPanel("body"),
    ]

    def get_topic_pages(self):
        return self.get_siblings().live().order_by("title")
