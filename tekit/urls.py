from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from feed import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('', include('feed.urls')),
    # Like comment
    path('like_comment/', views.like_comment, name='like_comment'),
    # like reply
    path('like_reply/', views.like_reply, name="like_reply"),
    # like feed
    path('like_feed', views.like_feed, name='like_feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
