from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib import messages
from django.dispatch import receiver



# Create your models here.


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return "%s - %s " % (self.text, self.owner.username)


# For user to record
class Feed(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'feeds'

    def __str__(self):
        """Return a string representation of the model"""
        # Showing the first 50 characters of text
        return f"{self.text[:50]}..."

# A temp table
class Temp(models.Model):
    """A temp table"""
    temp = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)


# Profile class inherit form User abstract class
class Profile(models.Model):
    """Store extract information relates to the user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    phone = models.CharField(max_length=15)
    birthdate = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=30)

    def clean_phone(self):
        phone = self.clean_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
           raise messages.error(request, 'Enter a valid phone number. e.g.555-555-5555')
        return self.clean_data['phone']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()        