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

from django.db.models import Q
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType

from PIL import Image
import json
from urllib.parse import quote_plus

from .models import *
from .forms import *

# Create your views here.

def index(request):
    """The home page for our Learning app """
    # We set how many hot topics and no hot topics to display
    max_hot_topics = 3
    max_topics_list = 3
    
    # hot topics
    hot_topics_list = Topic.topic.get_hot_topics()

    # not hot topics
    # topics_list = Topic.topic.get_not_hot_topics()
    topics_list = Topic.topic.get_latest_topic()
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
    topics = Topic.objects.filter(from_user=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'feed/topics.html', context)


@login_required
def show_all_topics(request):
    """Show all topics"""
    # topics = Topic.objects.order_by('date_added')

     # getting Topic Action id
    # t_action_id = TopicAction.objects.all().values('id')[0]['id']
    topics = Topic.objects.filter().select_related('action')[:100]
    #topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'feed/all_topics.html', context)



@login_required
def topic(request, pk):
    """Show a single topic and all its feeds"""
    topic = Topic.objects.get(id=pk)


    # Make sure the topic belongs to the current user
    # if topic.from_user != request.user:
    #     raise Http404
    
    # feed = Feed.objects.filter().select_related('topic')[:100]
    feed = Feed.objects.filter().select_related('topic').order_by('-date_posted')[:100]
    #feed = Topic.topic.order_by('-date_added')

    context = {'topic': topic, 'feeds': feed}
    return render(request, 'feed/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""
    # Test to determine whether the request is GET or POST
    if request.method == 'POST':
        topic_name = request.POST['topic_name']
        topicfile = request.FILES.get('topicfile')  # Avoiding duplicated dict keys.
        # topicfile = request.FILES.get['topicfile'] # This gives duplicated dict key
        # from_user = User.objects.get(id=request.user.id)
        profile = request.user.userprofile
        from_user = profile.user

        # creating topic 
        topic_action = TopicAction.objects.get_or_create(name=topic_name, image=topicfile)
        t_action_id = TopicAction.objects.all().order_by('-id').distinct('id')[:1]
        # print(t_action_id)
        # update topic table
        t = Topic()
        t.update_topic(from_user, t_action_id, None)

        topic = Topic.objects.order_by('id').last()
        t_id = topic.id

        messages.add_message(request, messages.INFO, 'Topic successfully created!')

        return HttpResponseRedirect(reverse('feed:topic', kwargs={ "pk":t_id }))

    else:
        return render(request, 'feed/new_topic.html')



# Show hot topics
def show_hot_topics(request):
    topics = Topic.objects.get_hot_topics()

    context = {'topics': topics}

    return render(request, 'feed/hot_topics.html', context)


@login_required
def new_feed(request, pk):
    """Add a new feed for a particular topic"""
    topic = Topic.objects.get(pk=pk)
    profile = request.user.userprofile
    view_by = profile
    # print(profile)
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
            nfeed.author = profile
            nfeed.view_by = view_by
            nfeed.save()
            # messages.success(request, '')
            messages.add_message(request, messages.INFO, 'Post submitted!')
            return redirect('feed:topic', pk=topic.id)

    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'feed/new_feed.html', context)


# Edit a feed
@login_required
def edit_feed(request, pk):
    """Edit an existing feed"""
    feed = Feed.objects.get(id=pk)
    topic = feed.topic

    # Protecting the edit feed page.
    if topic.from_user != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry
        form = FeedForm(instance=feed)
    else:
        # POST data submitted; process data
        form = FeedForm(request.POST, request.FILES, instance=feed)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Feed successfully updated')
            return redirect('feed:topic', pk=topic.id)

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
        raise messages.add_message(request, messages.ERROR, 'Feed not found')


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
    # comments = Comment.objects.filter(feed=feed, approved=True).order_by('-pk')
    comments = feed.comments.all().filter(approved=True).order_by('-created_on')
    is_liked = False
    reply = None
    profile = request.user.userprofile
    view_by = profile

    #user in obj.likes.all()
    # if feed.likes.filter(id=request.user.pk).exists():

    if request.method == 'POST':
        if 'replyForm' in request.POST:
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')

            reply_obj = None
            parent_qs = None
           
            # get parent comment id from hidden input
            try:
                parent_id = int(request.POST.get('parent_id'))
                # if parent_id exists
                if parent_id:
                    # get parent object by id
                    parent_qs = Comment.objects.get(id=parent_id)


                reply, created = Reply.objects.get_or_create(
                                                   user = profile.user,
                                                   content = content,
                                                   view_by = view_by,
                                                   parent= parent_qs,
                                                   )
                reply = get_object_or_404(Reply, pk=pk)
               
                if reply.likes.filter(id=request.user.id).exists():
                    is_liked = True
            except:
                pass

            messages.add_message(request, messages.SUCCESS, 'Reply sent!')
            # return redirect('feed:feed_detail', pk=feed.pk)
            return HttpResponseRedirect(reverse('feed:feed_detail', kwargs={ "pk":feed.pk }))

        else:
            print("replyForm form not found!")
   
    # comments = instance.comments
    context = {
         'feed': feed,
         'is_liked': is_liked,
         'total_likes': feed.get_total_likes(),
         'reply': reply,
         'comments': comments,
         # 'comment_form': comment_form
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
    profile = request.user.userprofile
    commented_by = profile
    view_by = profile

    # Comment posted
    if request.method == 'POST':
        content = request.POST.get('content')
        new_comment, created = Comment.objects.get_or_create(
                                                   user = profile.user,
                                                   content = content,
                                                   feed_id = feed.pk,
                                                   commented_by = commented_by,
                                                   view_by = view_by
                                                   )

        messages.add_message(request, messages.SUCCESS, 'Comment posted!')
        # return redirect('feed:feed_detail', pk=feed.pk)
        return HttpResponseRedirect(reverse('feed:feed_detail', kwargs={ "pk":feed.pk }))
        
       
      
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
    # return render(request, 'feed/feed_detail.html', context)



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
            messages.add_message(request, messages.SUCCESS, 'Comment updated')
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
    user = request.user.id
    # profile = request.user.userprofile
    comment = get_object_or_404(Comment, id = int(request.POST.get('id')))
    if comment.likes.filter(id=user).exists():
        comment.likes.remove(user)
        is_liked = False
    else:
        is_liked = True
        comment.likes.add(user)

    context = {
        'comment': comment,
        'is_liked': is_liked,
        'total_likes': comment.get_total_likes(),
        }
    if request.is_ajax():
        html = render_to_string('partials/like_section.html', context, request=request)
        return JsonResponse({"form": html})
        url_ = comment.get_absolute_url()
        return HttpResponseRedirect(reverse(url_))
        
    


def like_reply(request):
    user = request.user.id
    reply= get_object_or_404(Reply, id = int(request.POST.get('id')))
    if reply.likes.filter(id=user).exists():
        reply.likes.remove(user)
        is_liked = False
    else:
        is_liked = True 
        reply.likes.add(request.user.id)
    
    context = {
        'reply': reply,
        'is_liked': is_liked,
        'total_likes': reply.get_total_likes(),
        }
    if request.is_ajax():
        html = render_to_string('partials/like_reply_section.html', context, request=request)
        return JsonResponse({"form": html})
        url_ = reply.get_absolute_url()
        return HttpResponseRedirect(reverse(url_))



    

