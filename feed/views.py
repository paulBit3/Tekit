from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import  get_object_or_404
from django.contrib import messages
from django.utils import timezone

from PIL import Image

from .models import Topic, Feed, Comment
from .forms import TopicForm, FeedForm,CommentForm

# Create your views here.

def index(request):
    """The home page for our Learning app """
    feeds = Feed.objects.order_by('-date_added').filter(is_published=True)[:3]
    # topic = Topic.objects.get(id=topic_id)

    context = {
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
def topic(request, topic_id):
    """Show a single topic and all its feeds"""
    topic = Topic.objects.get(id=topic_id)

    # Make sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404

    feeds = topic.feed_set.order_by('-date_added')
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
            obj = form.save(commit=False)
            obj.owner = request.user  # we add the owner to the model after the form has validated, but before saving it
            obj.save()
            return redirect('feed:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'feed/new_topic.html', context)

@login_required
def new_feed(request, topic_id):
    """Add a new feed for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = FeedForm()
    else:
        # POST data submitted; process data
        form = FeedForm(request.POST, request.FILES)
        if form.is_valid():
            nfeed = Feed(image = request.FILES['image'])
            # nfeed = nfeed.rotate(18, expand=True)
            nfeed = form.save(commit=False)
            nfeed.topic = topic
            nfeed.save()
            messages.success(request, 'Your post has been submitted')
            return redirect('feed:topic', topic_id=topic_id)

    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'feed/new_feed.html', context)


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
def feeds(request, topic_id):

    try:
        feed = Feed.objects.all().filter(date_added=timezone.now()).order_by('-date_added')
        topic = Topic.objects.get(id=topic_id)
        #output = ''.join([q.text for q in feed])
    except Feed.DoesNotExist:
        raise messages.error('Feed not found!')

    context = {
        'feed': feed,
        'topic': topic
        }

    return render(request, 'feed/feed_list.html', context)

# Feed details
def feed_detail(request, feed_id):
    feed = get_object_or_404(Feed, feed_id=feed_id)
    return render(request, 'feed/feed_detail.html', {'feed': feed})


# adding comment to feed
def add_comment_feed(request, feed_id):
    feed = get_object_or_404(Feed, feed_id)

    # Comment posted
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create Comment object but don't save to database yet
            comment = form.save(commit=False)
            comment.feed = feed
            comment.save()
            return redirect('feed:feed_detail', feed_id=feed_id)

    else:
        form = CommentForm()
    return render(request, 'feed/add_comment.html', {'form': form})


# Comment approved method, if user are logged in
@login_required
def comment_approved(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('feed:feed_detail', pk=comment.feed.pk)



# Comment remove method, if uder are logged in
def comment_removed(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('feed:feed_detail', pk=comment.feed.pk)


# def feeds(request, topic_id):
#     """Show all feeds"""
#     feeds = Topic.objects.all().order_by('-date_added')

#     context = {
#         'topic': topic,
#         }

#     return render(request, 'feed/feed_list.html', context)

