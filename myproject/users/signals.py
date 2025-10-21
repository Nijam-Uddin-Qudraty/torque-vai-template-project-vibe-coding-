from .models import OtpToken
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from .models import OtpToken

def create_otp(user):
    """Creates or refreshes OTP for the user and emails it."""
    OtpToken.objects.filter(user=user).delete()

    otp_token = OtpToken.objects.create(
        user=user,
        expires_at=timezone.now() + timezone.timedelta(minutes=2)
    )

    User.objects.filter(pk=user.pk).update(is_active=False)

    subject = "Verification OTP"
    message = (
        f"Hi {user.username}, your OTP is {otp_token.otp}. "
        f"It will expire in 2 minutes.\n\n"
        f"Verify your account here: "
        f"http://127.0.0.1:8000/verify-otp/{user.username}/"
    )
    from_email = "nizamuddinqudrati@gmail.com"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

@receiver(post_save, sender=User)
def create_otp_on_user_creation(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        create_otp(instance)
