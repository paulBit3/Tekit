from django.contrib import admin
from django.urls import path, include

# Dealing with media
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('users/', include('accounts.urls')),
    path('', include('feed.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
