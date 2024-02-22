from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class NewsPost(Page):
    created_at = models.DateField("Post created at", auto_now_add=True)
    updated_at = models.DateField("Post updated at", auto_now=True)
    preview = models.TextField(max_length=350, blank=False, verbose_name="Preview text")
    body = RichTextField(blank=False)

    content_panels = Page.content_panels + [FieldPanel("preview"), FieldPanel("body")]

    def get_related_posts(self):
        return (
            NewsPost.objects.live()
            .sibling_of(self)
            .order_by("-created_at")
            .not_page(self)[:4]
        )


class NewsIndex(Page):
    def get_news_posts(self):
        return NewsPost.objects.live().descendant_of(self).order_by("-created_at")[:10]
