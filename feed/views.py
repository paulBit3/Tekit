from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import  get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from PIL import Image

from .models import Topic, Feed, Comment
from .forms import TopicForm, FeedForm,CommentForm

# Create your views here.

def index(request):
    """The home page for our Learning app """
    # We set how many hot topics and no hot topics to display
    max_hot_topics = 3
    max_topics_list = 2
    
    # hot topics
    hot_topics_list = Topic.objects.get_hot_topics()

    # not hot topics
    topics_list = Topic.objects.get_not_hot_topics()

    show_more_link_hot_topics = hot_topics_list.count() > max_hot_topics
    show_more_link_topics = topics_list.count() > max_topics_list

    feeds = Feed.objects.order_by('-date_added').filter(is_published=True)[:3]
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
            obj = Topic(image = request.FILES['image'])
            obj = form.save(commit=False)
            obj.owner = request.user  # we add the owner to the model after the form has validated, but before saving it
            obj.save()
            return redirect('feed:topics')

    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'feed/new_topic.html', context)


# Show hot topics
def show_hot_topics(request):
    topics = Topic.objects.get_hot_topics()

    context = {'topics': topics}

    return render(request, 'feed/hot_topics.html', context)


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
            nfeed.author = request.user
            nfeed.save()
            messages.success(request, 'Your post has been submitted')
            return redirect('feed:topic', topic_id=topic_id)

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
        feed = Feed.objects.all().order_by('-date_added')
        # topic = Topic.objects.get(pk=topic_id)
        #output = ''.join([q.text for q in feed])
    except Feed.DoesNotExist:
        raise messages.error('Feed not found!')


    context = {
        'feed': feed,
        # 'topic': topic
        }

    return render(request, 'feed/feed_list.html', context)


# Feed details
def feed_detail(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    comments = feed.comments.filter(approved=True).order_by('created_on')

    context = {
         'feed': feed,
         'comments': comments
         }

    return render(request, 'feed/feed_detail.html', context)


# adding comment to feed
@login_required
def add_comment_feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    comments = feed.comments.all().filter(approved=True).order_by('created_on')[:10]
    new_comment = None

    # Comment posted
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            new_comment.feed = feed    # Assign the current feed to the comment
            new_comment.user = request.user
            new_comment.save()  # Save comment to db
            return redirect('feed:feed_detail', pk=feed.pk)

    else:
        form = CommentForm()

    return render(request, 'feed/add_comment_feed.html', {'feed': feed,
                                                          'comments': comments,
                                                          'new_comment': new_comment,
                                                          'form': form
                                                          },)


# Comment approved method, if user are logged in
@login_required
def comment_approved(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('feed:feed_detail', pk=comment.feed.pk)



# Comment remove method, if uder are logged in
@login_required
def comment_removed(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
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

