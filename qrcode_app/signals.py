from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def send_login_notification(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    send_mail(
        'New Login Detected',
        f'New login detected for your account from IP: {ip}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )