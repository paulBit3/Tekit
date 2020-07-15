from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import MinLengthValidator

from PIL import Image


# Create your models here.

# A topic manager class as interface between Topic model and the db


class TopicManager(models.Manager):
    """A topic manager class"""

    # get all topics that has hot_topics set to True
    def get_hot_topics(self):
        return super().get_queryset().filter(hot_topics=True)

    # get all topics that has hot_topics set to False
    def get_not_hot_topics(self):
        return self.filter(hot_topics=False)

    # get all topics given a feed
    def get_by_feed(self, is_published):
        return super().get_queryset().filter(feed__is_published__iexact=feed)


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='topimages/',
        default= 'images/topicholder.png',
        max_length= 100
        )

    hot_topics = models.BooleanField(default=False)

    # Adding meta information about the model
    class Meta:
        ordering = ['-hot_topics']

    # An instance of TopicManager class
    objects = TopicManager()
    

    # Resizing topic photo
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

    def __str__(self):
        """Return a string representation of the model."""
        return '{} - {}'.format(self.text, self.owner.username)

    # Handling image location
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return "static/images/topic.jpg"


# For user to record
class Feed(models.Model):
    """Something specific learned about a topic"""
    STATUS = (
        (1, 'new'), (2, 'verified'), (3, 'published')
        )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')
    # likes = models.ManyToManyField(User, related_name='likes', blank=True)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    status = models.IntegerField(choices = STATUS, default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'feeds'

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

    # avoid keeping all photo loaded by user in the same folder
    def get_upload_path(instance, filename):
        return os.path.join('feed/photos/', now().date().strftime("%Y/%m/%d"), filename)

    def __str__(self):
        """Return a string representation of the model"""
        # Showing the first 50 characters of text
        return f"{self.text[:50]}..."
  
# Comment class
class Comment(models.Model):
    """Managing feeds or topic User comment about"""
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(validators=[MinLengthValidator(150)], blank=True)
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)  # to prevent spam

    class meta:
        """A meta class"""
        ordering = ['created_on']
    
    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count()

    # approve user comment before displaying
    def approve(self):
        self.approved = True
        self.save()

    def approved_comments(self):
        return self.comments.filter(approve=True)



    def __str__(self):
        return 'Comment {} - by {}'.format(self.comment, self.user.username)[:30]


# Like class to like a topic or a feed
# Assuming that many users can like many feeds
class Like(models.Model):
    """Class for Like"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='feeds', null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topics', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments', null=True)
    value = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'feed'
        unique_together = ['user','topic','feed','comment','value']

    def get_user_like(self):
        return  "User: ", self.user,  "comment:", self.salary, "value:", self.value


    # I use the __str__ function to show the user, feed, topic, comment, and value
    def __str__(self):
        return str(self.user) +':'+ str(self.comment) +':' + str(self.value)


# A temp table
class Temp(models.Model):
    """A temp table"""
    temp = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
