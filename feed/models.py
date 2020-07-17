from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import messages
from django.core.validators import MinLengthValidator

# the fields content_type , object_id , GenericForeignKey , 
# does not create additional database migrations.
from django.contrib.contenttypes.fields import GenericRelation

from django.db import models

from PIL import Image

# Using ContentType and GenericForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType




# The LikeDislikeManager() model manager 
class LikeDislikeManager(models.Manager):
    """Like Dislike model manager"""
    related_fields = True

    def likes(self):
        # taking record greater than 0
        return self.get_queryset().filter(rate__gt=0)

    def dislikes(self):
        # taking record less than 0
        return self.get_queryset().filter(rate__lt=0)

    # total rating methods
    def rating_sum(self):
         return self.get_queryset().aggregate(Sum('rate')).get('rate__sum') or 0


    """Implementing user behavior"""

    def comments(self):
        return self.get_queryset().filter(content_type__model='Comment').order_by('-created_on')


    def feeds(self):
        return self.get_queryset().filter(content_type__model='Feed').order_by('-date_added')


    def topics(self):
        return self.get_queryset().filter(content_type__model='Topic').order_by('-date_added')




"""Instead of creating several like and dislike methods,
I will create only one class LikeDislike.
The Like Dislike is based on the principle +1/-1"""

class LikeDislike(models.Model):
    """Like and Dislike class"""
    Like = 1
    Dislike = -1

    STATUS = (
        (Like, 'Like'), 
        (Dislike, 'Dislike')
        )

    rate = models.SmallIntegerField(verbose_name = "rates", choices=STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    date = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # primary key ID of the model instance for which the relationship is created
    object_id = models.PositiveIntegerField()

    # communication with any model
    content_object = GenericForeignKey('content_type', 'object_id')

    # An instance of LikeDislikeManager class
    objects = LikeDislikeManager()



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
    read_time = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='topimages/',
        default= 'images/topicholder.png',
        max_length= 100
        )
    rates = GenericRelation(LikeDislike, related_query_name ='topics')
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
    rates = GenericRelation(LikeDislike, related_query_name ='feeds')
    status = models.IntegerField(choices = STATUS, default=1)
    read_time = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'feeds'


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
    comment = models.TextField(validators=[MinLengthValidator(50)], blank=True)
    rates = GenericRelation(LikeDislike, related_query_name ='comments')
    read_time = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)  # to prevent spam

    class meta:
        """A meta class"""
        ordering = ['created_on']
    
    # def get_total_likes(self):
    #     return self.likes.users.count()

    # def get_total_dis_likes(self):
    #     return self.dis_likes.users.count()

    # approve user comment before displaying
    def approve(self):
        self.approved = True
        self.save()

    def approved_comments(self):
        return self.comment.filter(approve=True)


    def __str__(self):
        return 'Comment {} - by {}'.format(self.comment, self.user.username)[:30]



# A temp table
class Temp(models.Model):
    """A temp table"""
    temp = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
