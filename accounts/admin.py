from django.contrib import admin

# Register your models here.
from . models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name', 'phone_no']
	list_filter = ['status', 'phone_no']

admin.site.register(UserProfile, UserProfileAdmin)
		
