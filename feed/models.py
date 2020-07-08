from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages

from PIL import Image


# Create your models here.


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return '{} - {}'.format(self.text, self.owner.username)


# For user to record
class Feed(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='photos/%Y/%m/%d/' , blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    is_published = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'feeds'

    def __str__(self):
        """Return a string representation of the model"""
        # Showing the first 50 characters of text
        return f"{self.text[:50]}..."
    
    # to calculate likes
    @property
    def tottal_likes(self):
        """
        Likes for a feed or a topic
        :return: Integer: Likes for a feed or a topic
        """
        return self.likes.count()

      # Resizing the user profile photo
    def resize_image(self):
        SQUARE_FIT_SIZE = 300
        img = Image.open(self.image.path)
        
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
            img.save(self.iamge.path)


# Comment class
class Comment(models.Model):
    """Managing feeds or topic User comment about"""
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # to prevent spam

    class meta:
        """A meta class"""
        ordering = ['created_on']
    
    # approve user comment before displaying
    def approve(self):
        self.approved = True
        self.save()


    def __str__(self):
        return 'Comment {} - {}'.format(self.text, self.user.username)


# Like class to like a topic or a feed
# Assuming that many users can like many feeds
class Like(models.Model):
    """Class for Like"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='feeds')
    created_on = models.DateTimeField(auto_now_add=True)


# A temp table
class Temp(models.Model):
    """A temp table"""
    temp = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
