from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
from azure.communication.email import EmailClient
from ptuweb.settings import env
from .forms import SupportForm


def send_support_request_confirmation(form: SupportForm):
    full_name = form.cleaned_data["given_name"] + " " + form.cleaned_data["family_name"]
    body = f"Dear {full_name.title()},\n\n"
    body += "This is an automated email to let you know we have received your support request. "
    body += "We have included the details you provided below.\n\nWe will get back to you as soon as possible."
    body += "\n\nIn solidarity,\nPeterborough Tenants Union\n\n\n"
    body += " DETAILS ".center(50, "-")
    body += f"\n\n{str(form)}"

    message = EmailMessage(
        subject="Support request confirmation",
        to=(form.cleaned_data["email"],),
        reply_to=("support@peterboroughtenants.org",),
        body=body,
    )

    message.send()


def send_support_request_email(form: SupportForm):
    body = "A new request for support has been received, details below."
    body += "\n\n\n"
    body += " DETAILS ".center(50, "-")
    body += f"\n\n{str(form)}"

    message = EmailMessage(
        subject="New support request [URGENT]",
        to=("support@peterboroughtenants.org",),
        reply_to=(form.cleaned_data["email"],),
        body=body,
    )

    message.send()


class AzureEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages: list[EmailMessage]):
        connection_string = env("AZURE_EMAIL_CS")
        client = EmailClient.from_connection_string(connection_string)
        success_count = 0

        for message in email_messages:
            for r in message.recipients():
                message_data = {
                    "senderAddress": "automated@peterboroughtenants.app",
                    "recipients": {
                        "to": [{"address": r}],
                    },
                    "content": {
                        "subject": message.subject,
                        "plainText": message.body,
                    },
                }

                if len(message.reply_to) > 0:
                    message_data["replyTo"] = []
                    for r2 in message.reply_to:
                        message_data["replyTo"].append({"address": r2})

                poller = client.begin_send(message_data)
                result = poller.result()
                if result["status"] == "Succeeded":
                    success_count += 1
