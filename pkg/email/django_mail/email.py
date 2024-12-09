from typing import List, Optional

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from pkg.email.base import Email


class DjangoMail(Email):

    def send_mail(self, subject: str, body: str, receivers: List[str], sender: str, link: Optional[str] = None):
        # use a template for mail
        html_message = render_to_string(
            'notification/email-template.html', {"subject": subject, "body": body, "link": link})

        email = EmailMessage(subject=subject, body=html_message, from_email=sender, to=receivers)
        email.content_subtype = 'html'
        email.send()
