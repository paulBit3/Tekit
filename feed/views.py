from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from .models import Topic, Feed
from .forms import TopicForm, FeedForm

# Create your views here.

def index(request):
    """The home page for our Learning app """
    return render(request, 'feed/index.html')


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
        form = FeedForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.save()
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
        form = EntryForm(instance=feed)
    else:
        # POST data submitted; process data
        form = EntryForm(instance=feed, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feed successfully updated')
            return redirect('feed:topic', topic_id=topic.id)

    context = {'feed': feed, 'topic': topic, 'form': form}
    return render(request, 'feed/edit_feed.html', context)