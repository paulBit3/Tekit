from django.db import models

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from PIL import Image

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
    
    # Resizing the user profile photo
    def resize_image(self):
    	SQUARE_FIT_SIZE = 300
    	img = Image.open(self.photo.path)
        
        # Check if image needs to be resized.
    	if img.width > SQUARE_FIT_SIZE or img.height > SQUARE_FIT_SIZE:
    		# Calculate the new width and height to resize to
    		if width > height:
    			height = int((SQUARE_FIT_SIZE / width) * height)
    			width = SQUARE_FIT_SIZE
    		else:
    			width = int((SQUARE_FIT_SIZE / height) * width)
    			height = SQUARE_FIT_SIZE

    		# Resize the image
    		img = img.resize(width, height)
    		img.save(self.photo.path)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()     
