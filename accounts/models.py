from django.db import models

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.



# Profile class inherit form User abstract class
class Profile(models.Model):
    """Store extract information relates to the user model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    phone = models.CharField(max_length=20)
    birthdate = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    def clean_phone(self):
        phone = self.clean_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
           raise messages.error(request, 'Enter a valid phone number. e.g.555-555-5555')
        return self.clean_data['phone']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)
    instance.profile.save()     
