from django.contrib import admin

# Register your models here.
from . models import UserProfile, FollowUser

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['first_name']
	search_fields = ['first_name', 'phone_no']
	list_filter = ['status', 'phone_no']


class FollowUserAdmin(admin.ModelAdmin):
	list_display = ['created']
	search_fields = ['to_user', 'from_user']
	list_filter = ['to_user', 'from_user']



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FollowUser, FollowUserAdmin)
		
