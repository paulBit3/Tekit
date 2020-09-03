from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import *



@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
	if created:
		profile=UserProfile.objects.create(user = instance)
		followuser = FollowUser.objects.create(user = instance)
        profile.save()
        followuser.save()



@receiver(m2m_changed, sender=FollowUser.from_user.through)
def add_follower(sender, instance, action, reverse, pk_set, **kwargs):
	"""
      This signals will add a instance of user followed.
      Assuming that we have a user can follow 1 or many profiles
      A profile can be followed by 1 or many users
    """
	user_followed = []
    user_to_follow = User.objects.get(username = instance)
    #looping through the primary key subset
    for i in pk_set:
    	user = User.objects.get(pk = i)
        followuser_obj = FollowUser.objects.get(user = user)
        user_followed.append(followuser_obj)

    #looping the type of update that is done on the relation
    if action == "pre_add":
    	#looping in user followed list, if there is a user, add the user to follow
    	for i in user_followed:
    		i.to_user.add(user_to_follow)
            i.save()

    if action == "pre_remove":
    	#looping in user followed list, if there is a user, not follow again, remove it
    	for i in user_followed:
    		i.to_user.remove(user_to_follow)
            i.save()



