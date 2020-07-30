from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import messages
from django.core.validators import MinLengthValidator

# the fields content_type , object_id , GenericForeignKey , 
# does not create additional database migrations.
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from django.db import models
from accounts.models import UserProfile

from .utils import get_read_time
from PIL import Image

# Using ContentType and GenericForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



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


class TopicAction(models.Model):
    """a class that contains a type of each Topic"""

    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='topimages/',
        default= 'images/topicholder.png',
        max_length= 100
        )

        # Resizing topic photo
    def resize_image(self):
        SQUARE_FIT_SIZE = 300
        self.image = Image.open(self.image.path)
        
        # Check if image needs to be resized.
        if self.image.width > SQUARE_FIT_SIZE or self.image.height > SQUARE_FIT_SIZE:
            # Calculate the new width and height to resize to
            if width > height:
                height = int((SQUARE_FIT_SIZE / width) * height)
                width = SQUARE_FIT_SIZE
            else:
                width = int((SQUARE_FIT_SIZE / height) * width)
                height = SQUARE_FIT_SIZE

            # Resize the image
            self.image = self.image.resize(width, height)
            self.image.save(self.iamge.path) 
    

      # Handling image location
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return "static/topimages/topicholder.png"


    def __str__(self):
        """Return a string representation of the model."""
        return '{}'.format(self.name)
        


class Topic(models.Model):
    is_read = models.BooleanField(blank=True)
    read_time = models.PositiveSmallIntegerField(verbose_name='View Time', default=0)
    action = models.ForeignKey(TopicAction, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hot_topics = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # Adding meta information about the model
    class Meta:
        ordering = ['-hot_topics']

    # An instance of TopicManager class
    objects = models.Manager()
    topic= TopicManager()


    def get_total_likes(self):
        return self.likes.count()

    
    # Update topics
    def update_topic(self, from_user, action_id, to_user=None):
        action = TopicAction.objects(id=action_id)
        self = Topic(from_user=from_user, action=action, is_read=False)
        self.save()



    def __str__(self):
        """Return a string representation of the model."""
        return '{}'.format(self.owner.username)



# Feed publish manager
class PublishManager(models.Manager):
    """A Manager for publish feed"""
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')
        


# For user to record
class Feed(models.Model):
    """Something specific learned about a topic"""

    STATUS = (
        (1, 'new'), (2, 'verified'), (3, 'published')
        )
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField(max_length=160, blank=False, null=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')
    status = models.IntegerField(choices = STATUS, default=1)
    likes = models.ManyToManyField(User, blank=True, related_name='feed_likes')
    is_read = models.BooleanField(blank=True)
    read_time = models.PositiveSmallIntegerField(verbose_name='View Time', default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    view_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='feeds')
    
    
    class Meta:
        verbose_name_plural = 'feeds'

    objects = models.Manager()  # feed default manager
    published = PublishManager() # custom feed manager


    # Resizing the user profile photo
    def resize_image(self):
        SQUARE_FIT_SIZE = 300
        self.image = Image.open(self.image.path)
        
        # Check if image needs to be resized.
        if self.image.width > SQUARE_FIT_SIZE or self.image.height > SQUARE_FIT_SIZE:
            # Calculate the new width and height to resize to
            if width > height:
                height = int((SQUARE_FIT_SIZE / width) * height)
                width = SQUARE_FIT_SIZE
            else:
                width = int((SQUARE_FIT_SIZE / height) * width)
                height = SQUARE_FIT_SIZE

            # Resize the image
            self.image = self.image.resize(width, height)
            self.image.save(self.iamge.path)

    # avoid keeping all photo loaded by user in the same folder
    def get_upload_path(instance, filename):
        return os.path.join('feed/photos/', now().date().strftime("%Y/%m/%d"), filename)

    def get_absolute_url(self):
        return reverse('pages/', args=[self.id])

    def get_total_likes(self):
        return self.likes.count()

    def get_total_views(self):
        return self.views.count()

    def __str__(self):
        """Return a string representation of the model"""
        # Showing the first 50 characters of text
        return f"{self.text[:50]}..."
  

# Comment class
class Comment(models.Model):
    """Managing feeds or topic User comment about"""

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='likes')
    content = models.TextField(max_length=160, blank=False, null=False)
    commented_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='commented')
    reply = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    is_read = models.BooleanField(blank=True)
    read_time = models.PositiveSmallIntegerField(verbose_name='Read Time', default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    view_by = models.ForeignKey(UserProfile, verbose_name='View', on_delete=models.CASCADE, related_name='viewed')
    approved = models.BooleanField(default=False)  # to prevent spam

    class meta:
        """A meta class"""
        ordering = ['-date_added']
    
    # def get_total_likes(self):
    #     return self.likes.users.count()

    # def get_total_dis_likes(self):
    #     return self.dis_likes.users.count()

    # approve user comment before displaying
    def approve(self):
        self.approved = True
        self.save()

    def approved_comments(self):
        return self.content.filter(approve=True)

    def get_absolute_url(self):
        return reverse('feed:feed_detail', args=[self.id])

    def get_total_likes(self):
        return self.likes.count()

    def get_total_views(self):
        return self.views.count()


    def __str__(self):
        return 'Comment {} - by {}'.format(self.content, self.user.username)[:30]


# The LikeDislikeManager() model manager 
class LikeDislikeManager(models.Manager):
    """Like Dislike model manager"""

    def likes(self):
        # taking record greater than 0
        return self.get_queryset().filter(like__gt=0)

    def dislikes(self):
        # taking record less than 0
        return self.get_queryset().filter(like__lt=0)

    # total rating methods
    def total_likes(self):
         return self.get_queryset().aggregate(Sum('like')).get('like__sum') or 0


class LikeDislike(models.Model):
    """Like and Dislike class"""
    Like = 1
    Dislike = -1

    STATUS = (
        (Like, 'Like'), 
        (Dislike, 'Dislike')
        )
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="liked")
    feed = models.ForeignKey(Feed, null=True, blank=True, on_delete=models.CASCADE, related_name="likes_feed")
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE, related_name="likes_comment")
    value = models.SmallIntegerField(verbose_name = "likes", choices=STATUS, default=Like)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        """A Meta"""
        unique_together = ('feed', 'comment', 'liked_by',)
        ordering = ["-date"]
            

    # An instance of LikeDislikeManager class
    objects = LikeDislikeManager()


    def __str__(self):
 
        return '%s %s %f' % (self.liked_by, self.comment, self.feed, self.value)



class FollowUser(models.Model):
    """A FollowUser Class"""
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile')
    followed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed_by')

    def __str__(self):
        return "%s Followed by %s" % (self.profile, self.followed_by)


#Getting readtime
@receiver(pre_save, sender=Comment)
def pre_save_instance_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        read_time_var = get_read_time(instance.content)
        instance.read_time = read_time_var

pre_save.connect(pre_save_instance_receiver, sender=Comment)

# A temp table
class Temp(models.Model):
    """A temp table"""
    temp = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
