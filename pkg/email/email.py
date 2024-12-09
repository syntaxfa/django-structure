from functools import cache

from pkg.email.django_mail.email import DjangoMail


def django_email():
    return DjangoMail()


@cache
def get_email_service():
    return django_email()
