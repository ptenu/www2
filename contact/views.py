import random

from django.shortcuts import render
from .forms import ContactForm, SupportForm
import textwrap
from django.core.mail import EmailMessage
from ptuweb.settings.base import CONTACT_EMAIL
import secrets
from .turnstile import test_challenge
from .email import send_support_request_email, send_support_request_confirmation


def handle_contact_form(request):

    if not test_challenge(request.POST["cf-turnstile-response"]):
        raise Exception

    form = ContactForm(request.POST)

    ikey = request.POST["ikey"]
    has_sent = request.session[f"ikey_{ikey}"]
    if has_sent > 0:
        return render(request, "contact_form.html", {"form": form, "complete": True})

    if not form.is_valid():
        return render(request, "contact_form.html", {"form": form, "complete": False})

    # Create message string
    msg = "New website message (Contact Form):\n\n"
    msg += " MESSAGE ".center(60, "-")
    msg += "\n"
    msg += "From: ".ljust(15) + form.cleaned_data["name"] + "\n"
    msg += "Email: ".ljust(15) + form.cleaned_data["email"] + "\n"
    msg += "Message: ".ljust(15) + "\n"
    msg += textwrap.fill(form.cleaned_data["message"], width=60)

    msg += "\n" + " MESSAGE ENDS ".center(60, "-") + "\n"
    msg += "\n This is an automated email."

    email = EmailMessage(
        subject="New contact form submission",
        body=msg,
        to=(CONTACT_EMAIL,),
        reply_to=(form.cleaned_data["email"],),
    )

    email.send()
    request.session[f"ikey_{ikey}"] += 1

    return render(request, "contact_form.html", {"form": form, "complete": True})


def contact_form(request):
    if request.method == "POST":
        return handle_contact_form(request)

    # Create an idempotency key to prevent duplicate submissions
    ikey = secrets.token_urlsafe(12)
    request.session[f"ikey_{ikey}"] = 0
    return render(
        request,
        "contact_form.html",
        {"form": ContactForm(), "complete": False, "ikey": ikey},
    )


def contact_page(request):
    return render(request, "contact_page.html")


def help(request):
    return render(request, "help.html")


def handle_support_request_form(request):
    if not test_challenge(request.POST["cf-turnstile-response"]):
        raise Exception

    form = SupportForm(request.POST)
    if not form.is_valid():
        return render(
            request, "support_request.html", {"form": form, "complete": False}
        )

    # Send emails
    send_support_request_email(form)
    send_support_request_confirmation(form)

    return render(request, "support_request.html", {"form": form, "complete": True})


def support_request_form(request):
    if request.method == "POST":
        return handle_support_request_form(request)

    form = SupportForm()
    return render(request, "support_request.html", {"form": form, "complete": False})
