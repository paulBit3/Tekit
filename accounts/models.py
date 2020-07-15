from django.db import models

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

from PIL import Image

# Create your models here.



# Profile class inherit form User abstract class
class Profile(models.Model):
    """Store extract information relates to the user model"""
   
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="name")
    picture = models.ImageField(upload_to='images/profile_pic', blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    birthdate = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=50)
    status = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


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

