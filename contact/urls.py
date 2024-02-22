from django.urls import path

from . import views

contact_patterns = [path("", views.contact_page), path("form/", views.contact_form)]

help_patterns = [
    path("", views.help),
    path("support-request/", views.support_request_form),
]
