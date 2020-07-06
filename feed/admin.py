from django.contrib import admin

from .models import Topic, Feed, Profile

# Register your models here.

admin.site.register(Topic)
admin.site.register(Feed)
admin.site.register(Profile)

