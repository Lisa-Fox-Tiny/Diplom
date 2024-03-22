from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_password_reset_email(user_email, reset_password_token_key):
    msg = EmailMultiAlternatives(
        f"Password Reset Token",
        reset_password_token_key,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    msg.send()

@shared_task
def send_confirmation_email(user_email, confirmation_token_key):
    msg = EmailMultiAlternatives(
        f"Email Confirmation Token",
        confirmation_token_key,
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    msg.send()

@shared_task
def send_order_status_email(user_email):
    msg = EmailMultiAlternatives(
        f"Order Status Update",
        'Your order has been processed',
        settings.EMAIL_HOST_USER,
        [user_email]
    )
    msg.send()