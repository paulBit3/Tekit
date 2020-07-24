from django.contrib import admin

from .models import Topic, TopicAction, Feed, Comment, LikeDislike, UserProfile, FollowUser

# Register your models here.



class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'feed', 'date_added', 'approved')
	list_filter = ('approved', 'date_added', 'updated_at')
	search_fields = ('user', 'likes', 'content', 'reply')
	actions = ['approved_comment']

	# updating the active boolean field
	def approved_comment(self, request, queryset):
		queryset.updated(active=True)

class FollowUserAdmin(admin.ModelAdmin):
	list_display = ['profile', 'followed_by']
	search_fields = ['profile', 'followed_by']
	list_filter = ['profile', 'followed_by']


class LikeDislikeAdmin(admin.ModelAdmin):
	list_display = ['feed', 'comment', 'liked_by', 'value']
	search_fields = ['feed', 'comment', 'value']
	list_filter = ['date']
		


admin.site.register(Topic)
admin.site.register(TopicAction)
admin.site.register(Feed)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FollowUser, FollowUserAdmin)
admin.site.register(LikeDislike, LikeDislikeAdmin)
