# Tekit

🤔About the Project:

------

A social full-stack web application that makes easier for user to share technologies stories with friends, family. 
The app allows users to post, reply, like and comment, and share a topic.

-------
- Front-end techs stack: HTML, CSS, JavaScript, React 
- Back-end techs stack: Python/Django

------
- ```git clone: https://github.com/paulBit3/Tekit.git```

Features 
-
The App has a security algorithms implemented using JWT for authentication and authorization system for users to login and logout, and follow and un-follow others users. It also contains a password reset system which allows users to request a password reset link, which their receive in their email to reset their password. 
The App is deployed in AWS cloud Lightsail(A Virtual Private  server and Web Hosting).

Feature that Users can do:
-
- 1 - Post and comment on topic 
- 3 - Like and unlike a comment, Like a post
- 4 - Reply to comment
- 5 - Login and logout
- 6 - Comment words are limited		  			
---
- Authentication features are:
- 1 - Login and logout 
- 2 - User logout
- 3 - User modify profile
- 4 - Follow and un-follow friend
- 5 - Reset password
---
- Some others features are that:
- 1 - User receive reset link in their email accounts(Which ever email account)
- 2 - User can reset their password through a reset link
- 3 - User click on the reset link to reset their password
- 4 - User can be notified if the link has expired or alive.
-----

- Frontend
----
Templates
-
-------
Splash screen

```

{% block content %}

     <!-- Preloader Start -->
      <div id="preloader-active">
          <div class="preloader d-flex align-items-center justify-content-center">
              <div class="preloader-inner position-relative">
                  <div class="preloader-circle"></div>
                  <div class="preloader-img pre-text">
                    <img src="{% static 'images/social_discuss8.png' %}" alt="tekit-image">
                    <h3 class="">DigitX Inc.</h3>
                  </div>
              </div>
          </div>
      </div>
      <!-- End Preloader -->

     <!-- start sidebar -->
   <!--  <div id="sidebar">
    	 {#% include 'partials/_sidebar.html' %#}
    	 
    </div> -->
    <!-- end sidebar -->

  {% block sidebar %} {% endblock sidebar %}
```
-----
Comment page

```
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% load markdown_deux_tags %}

{% block content %}

  <div id="container">
	<div class="container">
		<div class="rows">
			<div class="col-lg-6 col-md-6 col-sm-6">
			  <div class="d-inline-flex bd-highlight">

	              <br>
				<div class="card-body">
				 	{% for comment in feed.comments.all %}
				 	 <!-- <div class="comments"> -->
				 	 	<p class="font-weight-bold">
				 	 		
					         {% if not comment.approved %}
						         <a href="{% url 'feed:comment_removed' pk=comment.pk %}">
						         	<i data-toggle="tooltip" data-placement="bottom" title="delete" class=" fas fa-times pr-2" aria-hidden="true"></i>
								 </a>
								 <a href="{% url 'feed:comment_approved' pk=comment.pk %}">
								 	<i data-toggle="tooltip" data-placement="bottom" title="approve" class=" fa fa-check pr-2" aria-hidden="true"></i>
						         </a>
				             {% endif %}

							 {#% if user.is_authenticated and comment.approved %#}
							  <!-- only allows user to delete his own comment -->
							 {% if  feed.comments.commented == request.user.userprofile and comment.approved %}
							   <a href="{% url 'feed:comment_removed' pk=comment.pk %}">
							   <i class="fa fa-trash"></i>
							   </a>
						     {% endif %}
				        </p>
				        <blockquote>

				         <small>Posted by:</small> <strong>{{ comment.user.username|capfirst }}</strong> - <small class="date text-muted">{{ comment.date_added}}</small>
				         <div id="captions">
				         	<div class="comment">
				         		<div class="caption" data-id="{{ comment.pk }}">
					         		<div class="usertext">
					         			 <!--  <p card-text>#{{ comment.content|slice:":300" }}</p> -->
									  	 <p class="mb-0"><small>{{ comment.content|markdown }}</small></p>
									        <!-- Comment like section -->
									        <div class="ml-1" id="like-section">
									         {% include 'partials/like_section.html' %}
										    </div>
										    <br>
									  	 	{% for reply in comment.replies.all %}
									  	 	<small>by <strong>{{ reply.user.username|capfirst }}</strong></small><p class="mb-0"><small>{{ reply.content|markdown }}</small></p>
									  	 	  <!-- Reply like section -->
									  	 	  <div id="like-reply-section">
									        	{% include 'partials/like_reply_section.html' %}
										      </div>
									  		{% endfor %}
									        
									  	 	<div class="panel-footer clearfix">
												<a href="" class="btn "><i class="fa fa-window-close" aria-hidden="true"></i>Cancel</a>

												<button class="reply-btn btn " type="button" data-id="{{ comment.pk }}"><i class="fa fa-reply-all"></i>Reply</button>
											</div>
				                            <div id="replyform-template" style="display: none;">
				                            <!-- <div class="comment-reply" style="display: none;"> -->
										 	    <form id="Form1" name="replyForm" action="{% url 'feed:feed_detail' feed.id %}" method="post">
											 	  	<input id="id-input" type="hidden" name="parent_id" value="{{ comment.pk }}">
											 	  	<div class="form-group">
											 	  		{% csrf_token %}
											 	  		<label for="reply">Reply:</label>
											 	  		<textarea id="contents" class="form-control form-rounded inputstl col-8" rows="2" type="text" name="content" placeholder="Replying... to {% if comment.user %} {{comment.user}} {% endif %}" required></textarea>
											 	  		<small id="charactersReplyLeft"></small>  
											 	  		<small id="repchar_count"></small>  
					                            		<!-- {{ form|crispy }} -->
											 	  		<!-- <textarea class="form-control" type="text" name="text"></textarea> -->
													   </div>
													<span><i class="fa fa-send sent-icon"></i></span>
											 	  	<input type="submit" class="btn btn-default pull-right reply" value="Send" name="replyForm">
											    </form>
									        </div>
					         		</div>
					         	</div>
				            </div>
				         </div>
				         
					  	 <p><small>Read time: {% if comment.read_time <= 1 %} < 1 Minute</small> {% else %}{{ comment.read_time }} minutes {% endif %}</p>
					  	 
						</blockquote>
				         <hr style='width:400px;'>
					     
					 <!-- </div> -->
					{% empty %}
					<p>No comments here yet :(</p>
					{% endfor %}
				</div>
			</div>
		  </div>
		</div>
	</div>
</div>

```
------

- Backend
--------
Models
-
```
#Topic table

class Topic(models.Model):
    is_read = models.BooleanField(blank=True)
    read_time = models.PositiveSmallIntegerField(verbose_name='View Time', default=0)
    action = models.ForeignKey(TopicAction, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_set1')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_set2', null=True)
    hot_topics = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # Adding meta information about the model
    class Meta:
        ordering = ['-hot_topics']

    # An instance of TopicManager class
    objects = models.Manager()
    topic= TopicManager()


    def get_total_likes(self):
        return self.likes.count()

    
    # Update topics
    def update_topic(self, from_user, action_id, to_user=None):
        action = TopicAction.objects.get(id=action_id)
        self = Topic(from_user=from_user, action=action, is_read=False, date_added=datetime.now())
        self.save()

    def get_absolute_url(self):
        return reverse('feed:topic', args=[self.id])

    def __str__(self):
        """Return a string representation of the model."""
        return '{}'.format(self.from_user.username)
```

```
#Reply table

class Reply(models.Model):
    """Reply Comment class"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies') # reply comment
    content = models.TextField(max_length=160, blank=False, null=False)
    likes = models.ManyToManyField(UserProfile, blank=True, related_name='r_likes')
    views = models.IntegerField(default=0)
    view_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='read')
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_public = models.BooleanField(default=False) # reply moderator

    class Meta:
        """A Meta class"""
        ordering = ['-date_added']
            


    def get_total_likes(self):
        return self.likes.count()
    
    def get_absolute_url(self):
        return reverse('feed:feed_detail', args=[self.id])

    def __str__(self):
        return 'Reply by {} - to {}'.format(self.user.username, str(self.parent))
```

```
# Profile class inherit form User abstract class
class UserProfile(models.Model):
    """Store extract information relates to the user model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=100, blank=True)
    last_name  = models.CharField(max_length=100, blank=True)
    about_me = models.TextField(max_length=150, blank=True)
    picture = models.ImageField(upload_to='images/pictures', default='images/pictures/user_default.png', blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True)
    dob = models.DateField(auto_now= False, auto_now_add=False, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    connection = models.CharField(max_length = 100, blank=True)
    follower = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

```

```
 # Methods to manage relationship between user
    def get_relationships(self):
        relationships = Relationship.objects.filter(
            models.Q(from_user=self.user) |
            models.Q(to_user=self.user)
            )
        return relationships
```



------
Demo screens

-------


![take_login_page](https://user-images.githubusercontent.com/43505777/92321495-1c0c9e80-eff0-11ea-939d-2a89db16d63b.JPG)
![tekit_registration_page_screen](https://user-images.githubusercontent.com/43505777/92321500-2890f700-eff0-11ea-9a8b-ad38b759524a.JPG)
![all_topics](https://user-images.githubusercontent.com/43505777/92321538-7ad21800-eff0-11ea-96ad-eaadd60ad182.gif)
![feed_list](https://user-images.githubusercontent.com/43505777/92321545-802f6280-eff0-11ea-90c8-e15defc930a3.gif)
![new_user_feed_create](https://user-images.githubusercontent.com/43505777/92321549-8a516100-eff0-11ea-87e1-444cef9d76e8.gif)
![topic_created](https://user-images.githubusercontent.com/43505777/92321553-8f161500-eff0-11ea-9747-48a7986be931.jpg)
![comment_chracters_check](https://user-images.githubusercontent.com/43505777/92321633-0ba8f380-eff1-11ea-84b4-5c8112faa9ea.gif)
![feed_comment](https://user-images.githubusercontent.com/43505777/92321638-0ea3e400-eff1-11ea-8518-3e503ac42351.gif)
![feed_comments_replying](https://user-images.githubusercontent.com/43505777/92321639-12d00180-eff1-11ea-9936-c306d6f4a1b4.gif)
![feed_updated](https://user-images.githubusercontent.com/43505777/92321644-1cf20000-eff1-11ea-99ea-cfc39bd9ab47.gif)
![feed_comment_liked](https://user-images.githubusercontent.com/43505777/92321678-75c19880-eff1-11ea-9e5d-6c97228e09d4.gif)
![like-comment-replies](https://user-images.githubusercontent.com/43505777/92321688-8e31b300-eff1-11ea-8de1-abae276d716a.gif)
![tekit_social_sharing](https://user-images.githubusercontent.com/43505777/92321763-334c8b80-eff2-11ea-9a98-c1e08f493ca6.JPG)
![user2_profile_details](https://user-images.githubusercontent.com/43505777/92321853-f339d880-eff2-11ea-898b-02171a8343e0.gif)
![user_profile_details](https://user-images.githubusercontent.com/43505777/92322026-61cb6600-eff4-11ea-9a10-0db5bbc478ab.JPG)
![tekit_follow_unfollow](https://user-images.githubusercontent.com/43505777/92322037-70b21880-eff4-11ea-8201-2caf432e7628.gif)
![activation_email_display](https://user-images.githubusercontent.com/43505777/92322150-2c734800-eff5-11ea-8eb8-9c71e2e70acf.gif)
![change_paswword](https://user-images.githubusercontent.com/43505777/92322153-2f6e3880-eff5-11ea-9d20-3ddcf745b414.gif)
![password_reset_complete](https://user-images.githubusercontent.com/43505777/92322157-3432ec80-eff5-11ea-9199-13df906b7004.gif)
![password_reset_field2](https://user-images.githubusercontent.com/43505777/92322161-385f0a00-eff5-11ea-9bd4-e840a55ec84b.gif)
![password_reset_sent](https://user-images.githubusercontent.com/43505777/92322168-3d23be00-eff5-11ea-8720-10dec8d9ac2b.gif)
![password_reset_unsuccessful](https://user-images.githubusercontent.com/43505777/92322171-401eae80-eff5-11ea-81db-810033129426.gif)
![password_reset1](https://user-images.githubusercontent.com/43505777/92322175-43199f00-eff5-11ea-9ed5-0b7b93728681.gif)
![password_reset2](https://user-images.githubusercontent.com/43505777/92322176-457bf900-eff5-11ea-8785-4ef0330e6f6a.gif)
![logout](https://user-images.githubusercontent.com/43505777/92322201-72c8a700-eff5-11ea-92b5-ab86c731f797.gif)
























![takeit-home-screen](https://user-images.githubusercontent.com/43505777/92321496-1ca53500-eff0-11ea-9b01-f270adb320b5.gif)


