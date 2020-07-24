from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from social.models import UserProfile

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwarg):
    if created:
        UserProfile.objects.create(user = instance, name=instance.username)