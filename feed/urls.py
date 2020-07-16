"""URL patterns for feed app"""

from django.urls import path

from .models import Topic, Feed, Comment, LikeDislike
from . import views

app_name = 'feed'

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows a topic
    path('topics/', views.topics, name='topics'),
    # Page to display  all topics
    path('topics/all/', views.show_all_topics, name='show_all_topics'),
    # Detail page for a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page for adding a new topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for showing hot topics
    path('topics/hot_topics/', views.show_hot_topics, name='show_hot_topics'),
    # Page for adding a new entry
    path('new_feed/<int:pk>/', views.new_feed, name='new_feed'),
    # Page for editing a post
    path('edit_feed/<int:feed_id>/', views.edit_feed, name='edit_feed'),
    # Page that shows all of the feeds
    path('feeds/', views.feeds, name='feeds'),
    # Page that shows all feed details
    path('feeds/<int:pk>/', views.feed_detail, name='feed_detail'),
    # Page that shows all comments related to a feed
    path('feeds/<int:pk>/comment/', views.add_comment_feed, name='add_comment_feed'),
    # Edit comment
    path('feeds/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    # Managing comment approved 
    path('comment/<int:pk>/approve/', views.comment_approved, name='comment_approved'),
    # Removing comment
    path('comment/<int:pk>/remove/', views.comment_removed, name='comment_removed'),
    # Like comment
    path('comment/<int:pk>/like/', views.RateView.as_view(model=Comment, rate_type=LikeDislike.Like), name='comnt_like'),
     # Dislike comment
    path('comment/<int:pk>/disllike/', views.RateView.as_view(model=Comment, rate_type=LikeDislike.Dislike), name='comnt_dislike'),
    # Like feed
    path('feed/<int:pk>/like/', views.RateView.as_view(model=Feed, rate_type=LikeDislike.Like), name='feed_like'),
     # Dislike feed
    path('fed/<int:pk>/dislike/', views.RateView.as_view(model=Feed, rate_type=LikeDislike.Dislike), name='feed_dislike'),
    # Like topic
    path('topic/<int:pk>/like/', views.RateView.as_view(model=Topic, rate_type=LikeDislike.Like), name='topic_like'),
     # Dislike topic
    path('topic/<int:pk>/dislike/', views.RateView.as_view(model=Topic, rate_type=LikeDislike.Dislike), name='topic_dislike'),
]