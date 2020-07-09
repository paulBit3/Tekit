"""URL patterns for feed app"""

from django.urls import path

from . import views

app_name = 'feed'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all topics
    path('topics/', views.topics, name='topics'),
    # Detail page for a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page for adding a new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for adding a new entry
    path('new_feed/<int:topic_id>/', views.new_feed, name='new_feed'),
    # Page for editing a post
    path('edit_feed/<int:feed_id>/', views.edit_feed, name='edit_feed'),
    # Page that shows all of the feeds
    path('feeds/', views.feeds, name='feeds'),
    # Page that shows all feed details
    path('feeds/<int:pk>/', views.feed_detail, name='feed_detail'),
    # Page that shows all comments related to a feed
    path('feeds/<int:pk>/comment/', views.add_comment_feed, name='add_comment_feed'),
    # Edit comment
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    # Managing comment approved 
    path('comment/<int:pk>/approve/', views.comment_approved, name='comment_approved'),
    # Removing comment
    path('comment/<int:pk>/remove/', views.comment_removed, name='comment_removed'),

]