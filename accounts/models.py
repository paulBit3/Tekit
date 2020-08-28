from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime
# from django.template.RequestContext

from PIL import Image

# Create your models here.



# Profile class inherit form User abstract class
class UserProfile(models.Model):
    """Store extract information relates to the user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    name = models.CharField(max_length=100)
    about_me = models.TextField(max_length=150)
    picture = models.ImageField(upload_to='images/pictures', default='images/pictures/user_default.png', blank=True, null=True)
    phone_no = models.CharField(max_length=15)
    birthdate = models.DateField(auto_now= False, auto_now_add=False, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=50)
    status = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)



    # Methods to manage relationship between user
    def get_relationships(self):
        relationships = Relationship.objects.filter(
            models.Q(from_user=self.user) |
            models.Q(to_user=self.user)
            )
        return relationships

    def has_relationship(self, visitor):
        """Check if a relation between two users exits"""
        relexit = Relationship.objects.filter(from_user=self.user, to_user=visitor)
        if not relexit:
            relexit = Relationship.objects.filter(from_user=visitor, to_user=self.user)
            if relexit:
                return True
            else:
                return False

    def get_friend_request(self):
        """getting a friend request"""
        frequest = RelationshipRequest.objects.filter(to_user=self.user)
        return frequest

    
    def has_request(self, visitor):
        """check if a user has sent a request"""
        has_sent_req = RelationshipRequest.objects.filter(from_user=visitor, to_user=self.user)
        if has_sent_req:
            return 'sent request'
        else:
            has_received_req = RelationshipRequest.objects.filter(from_user=self.user, to_user=visitor)
            if has_received_req:
                return 'receive request'
            else:
                return 'no request'


    # End methods for relashionship


    def clean_phone(self):
        phone_no = self.clean_data['phone_no']
        stripped_phone = strip_non_numbers(phone_no)
        if len(stripped_phone) < 10:
           raise messages.error(request, 'Enter a valid phone number. e.g.555-555-5555')
        # return self.clean_data['phone']
        return phone_no


    # Resizing the user profile photo
    def resize_image(self):
        SQUARE_FIT_SIZE = 300
        self.picture = Image.open(self.picture.path)
        
        # Check if image needs to be resized.
        if self.picture.width > SQUARE_FIT_SIZE or self.picture.height > SQUARE_FIT_SIZE:
            # Calculate the new width and height to resize to
            if width > height:
                height = int((SQUARE_FIT_SIZE / width) * height)
                width = SQUARE_FIT_SIZE
            else:
                width = int((SQUARE_FIT_SIZE / height) * width)
                height = SQUARE_FIT_SIZE

            # Resize the image
            self.picture = self.picture.resize(width, height)
            self.picture.save(self.picture.path)


    def next_birthday(born):
        today = date.today()

        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[self.id])


    def __str__(self):
        return f'{self.user.username} Profil'


class FollowUser(models.Model):
    """A FollowUser Class"""
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='profile')
    followed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed_by')

    def __str__(self):
        return "%s Followed by %s" % (self.profile, self.followed_by)


class RelationshipType(models.Model):
    """relationship type """
    name = models.CharField(max_length=50)

    def __str__(self):

        return self.name
        


class Relationship(models.Model):
    """Manage relationship between users"""

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationship_set1')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationship_set2')
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    created_at = models.DateTimeField('created_at', default=datetime.now())

    def __str__(self):
        return '%s, %s, %s' %(self.from_user.username,
                              self.to_user.username,
                              self.relationship_type.name)


class RelationshipRequest(models.Model):

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationship_request_set1')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relationship_request_set2')
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField('created at', default=datetime.now())

    def __str__(self):
        return '%s, %s' % (self.from_user.username, self.to_user.username)