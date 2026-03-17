from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if not created:
        return

    # ❌ Skip superusers & staff
    if instance.is_superuser or instance.is_staff:
        return

    profile = Profile.objects.create(
        user=instance,
        name=instance.username,
        email=instance.email,
    )

    # ✅ Email must NEVER break logic
    if settings.DEBUG:
        return

    try:
        send_mail(
            "Welcome to DevSearch",
            "We are glad you're here!",
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=True,
        )
    except Exception:
        pass


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    # ✅ Safe delete check
    if instance.user and not instance.user.is_superuser:
        instance.user.delete()
