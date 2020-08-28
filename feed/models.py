from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
# the fields content_type , object_id , GenericForeignKey , 
# does not create additional database migrations.
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from datetime import datetime
from django.urls import reverse

from django.db.models import Q
from django.db import models
from accounts.models import UserProfile


from markdown_deux import markdown
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

    def get_latest_topic(self, limit=100):
        #get a limit (default 100) latest topic
        topics = Topic.objects.filter(hot_topics=False).order_by('date_added')[:limit]
        return topics


class TopicAction(models.Model):
    """a class that contains a type of each Topic"""

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='topimages/', default='images/topicholder.png', null=True, blank=True, max_length=100)

    # Resizing topic photo
    def resize_image(self):
        SQUARE_FIT_SIZE = 300
        img = Image.open(self.image)
        width, height = img.size
        
        # Check if image needs to be resized.
        if width > SQUARE_FIT_SIZE or height > SQUARE_FIT_SIZE:
            # Calculate the new width and height to resize to
            if width > height:
                height = int((SQUARE_FIT_SIZE / width) * height)
                width = SQUARE_FIT_SIZE
            else:
                width = int((SQUARE_FIT_SIZE / height) * width)
                height = SQUARE_FIT_SIZE

            # Resize the image
            output_size = (width, height)
            # img = img.resize(width, height)
            img = img.thumbnail(output_size)
            if img is not None:
                img.save(img) 
        
        super(TopicAction, self).save(*args, **kwargs)

      # Handling image location
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "static/topimages/topicholder.png"

    #getting the topic name
    def get_topic(self):
        if self.name:
            return self.name
    

    def __str__(self):
        """Return a string representation of the model."""
        return '{}'.format(self.name)
        


class Topic(models.Model):
    is_read = models.BooleanField(blank=True)
    read_time = models.PositiveSmallIntegerField(verbose_name='View Time', default=0)
    action = models.ForeignKey(TopicAction, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_set1')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_set2', null=True)
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
        action = TopicAction.objects.get(id=action_id)
        self = Topic(from_user=from_user, action=action, is_read=False, date_added=datetime.now())
        self.save()

    def get_absolute_url(self):
        return reverse('feed/topic', args=[self.id])

    def __str__(self):
        """Return a string representation of the model."""
        return '{}'.format(self.from_user.username)



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
    image = models.ImageField(null=True, blank=True, upload_to='photos/%Y/%m/%d/', default='photos/feedholder.png')
    status = models.IntegerField(choices = STATUS, default=1)
    likes = models.ManyToManyField(User, blank=True, related_name='feed_liked')
    is_read = models.BooleanField(blank=False, default=False)
    read_time = models.PositiveSmallIntegerField(verbose_name='View Time', default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    view_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='feeds_viewed')
    
    
    class Meta:
        verbose_name_plural = 'feeds'

    objects = models.Manager()  # feed default manager
    published = PublishManager() # custom feed manager


    # Resizing the user profile photo
    def save(self, *args, **kwargs):
        SQUARE_FIT_SIZE = 300
        # img_path = settings.MEDIA_ROOT
        img = Image.open(self.image)
        # print(img)
        width, height = img.size

        # Check if image needs to be resized.
        if width > SQUARE_FIT_SIZE or height > SQUARE_FIT_SIZE:
            # Calculate the new width and height to resize to
            if width > height:
                height = int((SQUARE_FIT_SIZE / width) * height)
                width = SQUARE_FIT_SIZE
            else:
                width = int((SQUARE_FIT_SIZE / height) * width)
                height = SQUARE_FIT_SIZE

            # Resize the image
            # img = img.resize(width, height)
            output_size = (width, height)
            print(output_size)
            img = img.thumbnail(output_size)
            if img is not None:
                img.save(img)

        super(Feed, self).save(*args, **kwargs) 


   # approve user feed reed displaying
    def isread(self):
        self.is_read = True
        self.save()

    # avoid keeping all photo loaded by user in the same folder
    def get_upload_path(instance, filename):
        return os.path.join('feed/photos/', now().date().strftime("%Y/%m/%d"), filename)

    def get_absolute_url(self):
        return reverse('feed/feed_detail', args=[self.id])

    def get_total_likes(self):
        return self.likes.count()

    def get_total_views(self):
        return self.views.count()

    def get_latest_feed(self, limit=100):
        #get a limit (default 100) latest feeds
        feeds = Feed.objects.order_by('date_posted')[:limit]
        return feeds

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
    content = models.TextField(validators=[MaxLengthValidator(160)], blank=False, null=False)
    commented_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='commented')
    is_read = models.BooleanField(blank=True, default=False)
    read_time = models.PositiveSmallIntegerField(verbose_name='Read Time', default=0)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    views = models.IntegerField(default=0)
    view_by = models.ForeignKey(UserProfile, verbose_name='View', on_delete=models.CASCADE, related_name='viewed')
    approved = models.BooleanField(default=True)   # manually deactivate inappropriate comments from admin site
    is_public = models.BooleanField(default=False) # comment moderator
    # approved = models.BooleanField(default=True)  # to prevent spam

    # objects= CommentManager()

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

    # user comment read 
    def isread(self):
        self.is_read = True
        self.save()

    def approved_comments(self):
        return self.content.filter(approve=True)

    def get_absolute_url(self):
        return reverse('feed:feed_detail', args=[self.id])

    def get_total_likes(self):
        return self.likes.count()

    def get_total_views(self):
        return self.views.count()

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    # def children(self):   
    #     # Return replies of a comment
    #     return Comment.objects.filter(parent=self)


    # @property
    # def is_parent(self):
    #     # Return True if instance is a parent
    #     if self.parent is not None:
    #         return False
    #     return True
    
    def comments(self):
        instance = self
        query_set = Comment.objects.filter_by_instance(instance)

    def __str__(self):
        return 'Comment {} - by {}'.format(self.content, self.user.username)[:30]


class Reply(models.Model):
    """Reply Comment class"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies') # reply comment
    content = models.TextField(max_length=160, blank=False, null=False)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='r_likes')
    views = models.IntegerField(default=0)
    view_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='read')
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_public = models.BooleanField(default=False) # reply moderator

    class Meta:
        """A Meta class"""
        ordering = ['-date_added']
            


    def get_total_likes(self):
        return self.likes.count()


    def __str__(self):
        return 'Reply by {} - to {}'.format(self.user.username, str(self.parent))
        

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


#Getting readtime
@receiver(pre_save, sender=Comment)
def pre_save_comment_receiver(sender, instance, *args, **kwargs):
    if instance.content:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time

pre_save.connect(pre_save_comment_receiver, sender=Comment)
# pre_save.connect(pre_save_instance_receiver, sender=Comment)



# A temp table
class Temp(models.Model):
    """A temp table"""
    temp = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
