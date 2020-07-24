from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import  get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.views.generic import RedirectView
from django.views.generic.base import RedirectView
from django.views import View 
from django.urls import reverse

from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from PIL import Image
import json
from urllib.parse import quote_plus

from .models import Topic, Feed, Comment, LikeDislike
from .forms import TopicForm, FeedForm, CommentForm

# Create your views here.

def index(request):
    """The home page for our Learning app """
    # We set how many hot topics and no hot topics to display
    max_hot_topics = 3
    max_topics_list = 2
    
    # hot topics
    hot_topics_list = Topic.topic.get_hot_topics()

    # not hot topics
    topics_list = Topic.topic.get_not_hot_topics()

    show_more_link_hot_topics = hot_topics_list.count() > max_hot_topics
    show_more_link_topics = topics_list.count() > max_topics_list

    feeds = Feed.objects.order_by('-date_posted').filter(status=1)[:3]
    # topic = Topic.objects.get(id=topic_id)

    context = {
        'hot_topics_list': hot_topics_list[:max_hot_topics],
        'topics_list': topics_list[:max_topics_list],
        'show_more_link_topics': show_more_link_topics,
        'show_more_link_hot_topics': show_more_link_hot_topics,
        'feeds': feeds,
    }
    return render(request, 'pages/index.html', context)


# Restricting Access to the Topic Page
@login_required
def topics(request):
    """Show all topics"""
    # topics = Topic.objects.order_by('date_added')

    # Retrieve only the Topic whose owner attribute matches the current user
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'feed/topics.html', context)


@login_required
def show_all_topics(request):
    """Show all topics"""
    # topics = Topic.objects.order_by('date_added')

    # Retrieve only the Topic whose owner attribute matches the current user
    topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'feed/all_topics.html', context)



@login_required
def topic(request, topic_id):
    """Show a single topic and all its feeds"""
    topic = Topic.objects.get(id=topic_id)

    # Make sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404

    feeds = topic.feed_set.order_by('-date_posted')
    context = {'topic': topic, 'feeds': feeds}
    return render(request, 'feed/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""
    # Test to determine whether the request is GET or POST
    if request.method != 'POST':
        # No data submitted, it will create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            if form.is_multipart():
                # getting the image object if exist
                pic = request.FILES.get('image')
                obj = Feed(pic)
            # obj = Topic(image = request.FILES['image'])
            obj = form.save(commit=False)
            obj.owner = request.user  # we add the owner to the model after the form has validated, but before saving it
            obj.save()
            return redirect('feed:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'feed/new_topic.html', context)


# Update topics
def update_topic(self, action_id , owner):
    action = TopicAction.objects(id=action_id)
    self = Topic(owner=owner, action=action, is_read=False, date_added=datetime.now())
    self.save()


# Show hot topics
def show_hot_topics(request):
    topics = Topic.objects.get_hot_topics()

    context = {'topics': topics}

    return render(request, 'feed/hot_topics.html', context)


@login_required
def new_feed(request, pk):
    """Add a new feed for a particular topic"""
    topic = Topic.objects.get(pk=pk)

    if request.method != 'POST':
        form = FeedForm()
    else:
        # POST data submitted; process data
        form = FeedForm(request.POST, request.FILES)
        if form.is_valid():
            if form.is_multipart():
                # getting the image object if exist
                pic = request.FILES.get('image')
                nfeed = Feed(pic)
            
            # nfeed = nfeed.rotate(18, expand=True)
            nfeed = form.save(commit=False)
            nfeed.topic = topic
            nfeed.author = request.user
            nfeed.save()
            messages.success(request, 'Your post has been submitted')
            return redirect('feed:topic', pk=topic.id)

    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'feed/new_feed.html', context)


# Edit a feed
@login_required
def edit_feed(request, feed_id):
    """Edit an existing feed"""
    feed = Feed.objects.get(id=feed_id)
    topic = feed.topic

    # Protecting the edit feed page.
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry
        form = FeedForm(instance=feed)
    else:
        # POST data submitted; process data
        form = FeedForm(instance=feed, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feed successfully updated')
            return redirect('feed:topic', topic_id=topic.id)

    context = {'feed': feed, 'topic': topic, 'form': form}
    return render(request, 'feed/edit_feed.html', context)



# Displaying all new posts or feeds
def feeds(request):

    try:
        # feed = Feed.objects.all().filter(date_added=timezone.now()).order_by('-date_added')
        feed = Feed.objects.all().order_by('-date_posted')
        # topic = Topic.objects.get(pk=topic_id)
        #output = ''.join([q.text for q in feed])
    except Feed.DoesNotExist:
        raise messages.error('Feed not found!')


    context = {
        'feed': feed,
        # 'topic': topic
        }

    return render(request, 'feed/feed_list.html', context)


# Getting latest feeds
def get_latest_feed(self, limit=100):
    feeds = Feed.objects.order_by('date_posted')[:limit]
    return feeds




# Feed details
def feed_detail(request, pk):
   
    feed = get_object_or_404(Feed, pk=pk)
    comments = Comment.objects.filter(feed=feed, reply=None, approved=True).order_by('-pk')
    #comments = feed.comments.filter(approved=True).order_by('-created_on')
    is_liked = False
    #user in obj.likes.all()
    if feed.likes.filter(id=request.user.pk).exists():
        is_liked = True

    # getting comment reply
    if request.method == 'POSt':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(pk=reply_id)
                comment = Comment.objects.create(feed=feed, user=request.user, content=content, reply=comment_qs)
                comment.save()
    else:
        comment_form = CommentForm()

    context = {
         'feed': feed,
         'is_liked': is_liked,
         'total_likes': feed.get_total_likes(),
         'comments': comments,
         'comment_form': comment_form
         }
    if request.is_ajax():
        html = render_to_string('feed/comments.html', context, request=request)
        return JsonResponse({'form': html})

    return render(request, 'feed/feed_detail.html', context)
    #return HttpResponseRedirect(redirect_to="")


# adding comment to feed
@login_required
def add_comment_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    comments = feed.comments.all().filter(approved=True).order_by('date_added')[:10]
    new_comment = None
    com_submitted = False

    # Comment posted
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            new_comment.feed = feed    # Assign the current feed to the comment
            new_comment.user = request.user
            new_comment.save()  # Save comment to db
            # messages.success(request, 'Comment posted')
            return HttpResponseRedirect('/feed_detail?com_submitted=True', pk=feed.pk)
    else:
        form = CommentForm()
        if 'com_submitted' in request.GET:
            com_submitted = True
    context = {
         'feed': feed, 
         'comments': comments, 
         'new_comment': new_comment, 
         'form': form,
         'com_submitted': com_submitted
    }   


    return render(request, 'feed/add_comment_feed.html', context)



def like_feed(request):

    feed= get_object_or_404(Feed, id=request.POST.get('id'))

    is_liked = False
    # if user in comment.likes.all():
    #     comment.likes.remove(user)
    #     is_liked = False
    if feed.likes.filter(id=request.user.id).exists():
        feed.likes.remove(request.user)
        is_liked = False
    else:
        feed.likes.add(request.user)
        is_liked = True  

    context = {
         'feed': feed,
         'is_liked': is_liked,
         'total_likes': feed.get_total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('partials/like_feed_section.html', context, request=request)
        return JsonResponse({"form": html})

    # url_ = obj.get_absolute_url()
    # return HttpResponseRedirect(url_)



# Comment approved method, if user are logged in
@login_required
def comment_approved(request, pk):
    comment = get_object_or_404(Comment, pk=comment.pk)
    comment.approve()
    return redirect('feed:feed_detail', pk=comment.feed.pk)



# Comment remove method, if uder are logged in
@login_required
def comment_removed(request, pk):
    comment = get_object_or_404(Comment, pk=comment.pk)
    comment.delete()
    return redirect('feed:feed_detail', pk=comment.feed.pk)


# Edit comment
@login_required
def edit_comment(request, pk):
    """Edit an existing comment"""
    comment = get_object_or_404(Comment, pk=pk)
    feed = comment.feed
    
    # Protecting the edit feed page.
    if comment.user != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry
        form = CommentForm(instance=comment)
    else:
        # POST data submitted; process data
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated')
            return redirect('feed:feed_detail', pk=feed.pk)

    context = {'feed': feed, 'comment': comment, 'form': form}
    return render(request, 'feed/edit_comment.html', context)



# def feeds(request, topic_id):
#     """Show all feeds"""
#     feeds = Topic.objects.all().order_by('-date_added')

#     context = {
#         'topic': topic,
#         }

#     return render(request, 'feed/feed_list.html', context)
#-------------------------


def like_comment(request):
    user = request.user


    if request.method == 'POST':
        comment_id = request.POST.get('id')
        #comment_obj = Comment.objects.get(id=comment_id)
        comment_obj = get_object_or_404(Comment, id=comment_id)
        

        is_liked = False
     
        if comment_obj.likes.filter(id=user.id).exists():
            comment_obj.likes.remove(user)
            is_liked = False
        else:
            comment_obj.likes.add(user)
            like, created = LikeDislike.objects.get_or_create(user=user, comment_id=comment_id)
            if not created:
                if like.value == 1:
                    like.value -= 1;
                else:
                    like.value += 1
            like.save()
            is_liked = True  
            print(like)
        context = {
             'post': comment_obj,
             'is_liked': is_liked,
             'total_likes': comment_obj.get_total_likes(),
        }
        print(comment_obj)
        print(valueobj)
        print(comment_obj.get_total_likes())
        if request.is_ajax():
            html = render_to_string('partials/like_section.html', context, request=request)
            return JsonResponse({"form": html})

        url_ = obj.get_absolute_url()
        return HttpResponseRedirect(url_)



    


    

