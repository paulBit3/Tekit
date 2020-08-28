from django.contrib import admin

# Register your models here.
from . models import UserProfile, FollowUser

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name', 'phone_no']
	list_filter = ['status', 'phone_no']


class FollowUserAdmin(admin.ModelAdmin):
	list_display = ['profile', 'followed_by']
	search_fields = ['profile', 'followed_by']
	list_filter = ['profile', 'followed_by']



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FollowUser, FollowUserAdmin)
		
