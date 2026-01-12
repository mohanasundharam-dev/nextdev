from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender,instance,created,**kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email,
        )
        
        subject = "Welcome to DevSearch"
        message="We are Glad you here!"
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )
def deleteUser(sender,instance,**kwargs):
    user=instance.user
    user.delete()

post_save.connect(createProfile,sender=User)
post_delete.connect(deleteUser,sender=Profile)