from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from netology_pd_diplom.celery import app

# формирование и отправка писем перенесены из signals.py в tasks.py для применения в celery

@app.task()
def send_email(email, title, massage):

    msg = EmailMultiAlternatives(
        # title:
        title,
        # message:
        massage,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [email]
    )
    msg.send()
