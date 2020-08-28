from django.contrib import admin

from .models import Topic, TopicAction, Feed, Comment, Reply, LikeDislike, UserProfile

# Register your models here.



class CommentAdmin(admin.ModelAdmin):
	list_display = ('user', 'feed', 'date_added', 'approved')
	list_filter = ('approved', 'date_added', 'updated_at', 'is_public')
	search_fields = ('user', 'likes', 'content')
	actions = ['approved_comment', 'is_public']

	# updating the active boolean field to true
	def approved_comment(self, request, queryset):
		queryset.updated(approved=True)

class ReplyAdmin(admin.ModelAdmin):
	list_display = ('user', 'parent')
	list_filter = ('date_added', 'is_public')
	search_fields = ('user', 'content', 'parent')
	actions = ['is_public']



class LikeDislikeAdmin(admin.ModelAdmin):
	list_display = ['feed', 'comment', 'liked_by', 'value']
	search_fields = ['feed', 'comment', 'value']
	list_filter = ['date']
		


admin.site.register(Topic)
admin.site.register(TopicAction)
admin.site.register(Feed)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(LikeDislike, LikeDislikeAdmin)
