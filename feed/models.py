from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages

from PIL import Image


# Create your models here.

# A topic manager class as interface between Topic model and the db
class TopicsManager(models.Manager):
    """A topic manager class"""

    # get all topics that has hot_topics set to True
    def get_not_hot_topics(self):
        return self.filter(hot_topics=True)

    # get all topics that has hot_topics set to False
    def get_hot_topics(self):
        return self.filter(hot_topics=False)

    # get all topics given a feed
    def get_by_feed(self, is_published):
        return self.filter(feed__is_published__iexact=feed)


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hot_topics = models.BooleanField(default=False)

    # Adding meta information about the model
    class Meta:
        ordering = ['-hot_topics']

    # An instance of TopicManager class
    objects = TopicsManager()
            

    def __str__(self):
        """Return a string representation of the model."""
        return '{} - {}'.format(self.text, self.owner.username)


# For user to record
class Feed(models.Model):
    """Something specific learned about a topic"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/' , blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    is_published = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'feeds'

    def __str__(self):
        """Return a string representation of the model"""
        # Showing the first 50 characters of text
        return f"{self.text[:50]}..."
    
    # to calculate likes
    @property
    def total_likes(self):
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

    def approved_comments(self):
        return self.comments.filter(approve=True)



    def __str__(self):
        return 'Comment {} - by {}'.format(self.text, self.user.username)


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
