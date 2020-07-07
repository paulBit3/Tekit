from django.contrib import admin

from .models import Topic, Feed, Comment

# Register your models here.

admin.site.register(Topic)
admin.site.register(Feed)
admin.site.register(Comment)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'feed', 'text', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	actions = ['approved_comment']

	# updating the active boolean field
	def approved_comment(self, request, queryset):
		queryset.updated(active=True)