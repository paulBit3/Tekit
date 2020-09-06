from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
import json
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from .tokens import account_activation_token
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from .forms import *
from feed.models import *
from accounts.models import *

# Create your views here.
@login_required
def profile_detail(request, pk):
    """Method for user profile detail"""
    profile = request.user.userprofile
    user_relationships = profile.get_relationships()
    user_request = profile.get_friend_request()

    context = {
         # 'user': user,
         'profile': profile,
         'user_relationships': user_relationships,
         'user_request': user_request
    }

    return render(request, 'accounts/profile_detail.html', context)


@login_required
def get_user_profile(request, username):
    user_obj = User.objects.filter(username=username)
    
    
    # if request.user.username != user.username:
    #     raise Http404

    if user_obj:
        user_obj = user_obj[0]
        profile = UserProfile.objects.get(user=user_obj)
        conn = profile.connection
        followuser_obj = FollowUser.objects.get(user = user_obj)
        # followuser_obj = FollowUser.objects.get(user = user)
        follower, following = profile.follower, followuser_obj.from_user.count()
        is_following = FollowUser.objects.filter(user = request.user, from_user = user_obj)
        print(profile)
        print(conn)
        print(follower)
        print(following)
    
    context = {
           'profile': profile,
           'conn':conn, 
           'follower': follower, 
           'following': following, 
           'is_following': is_following 
           }
    return render(request, 'accounts/userprofile.html', context)


# profile update view.
@login_required
def profile_update(request, pk):
    user = User.objects.get(pk=pk)
    # profile = UserProfile(user = user)
    profile = request.user.userprofile
    profile_form = UserProfileInfoForm(instance=profile)
    
    if request.method == 'POST':
        profile_form = UserProfileInfoForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            #save user profile info
            profile_form.save()

            messages.add_message(request, messages.INFO, 'Your profile has been updated !')
            # return redirect('accounts:profile_detail', pk=pk)
            return HttpResponseRedirect(reverse('accounts:profile_detail', kwargs={ "pk":pk, }))
    else:
        profile_form = UserProfileInfoForm(instance=profile)
    context = {"form": profile_form,}
    return render(request, "accounts/profile_update.html", context)
 




# Class view to display list of members

@method_decorator(login_required, name='dispatch')
class ProfileListView(ListView):
    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Member'
        return context

    def get_queryset(self):
        profList = UserProfile.objects.all().order_by("-user_id");
        
        for uprofile in profList:
            uprofile.followed = False
            obj = FollowUser.objects.filter(user = uprofile.user.id, from_user=self.request.user.userprofile.user.id)
            if obj:
                uprofile.followed = True
        return profList




@login_required
def edit_profile(request):
    try:
        profile = request.user.get_profile()
    except:
        uprofile = UserProfile(user=request.user)
        uprofile.save()
        profile = request.user.get_profile()

    if request.method == 'POST':
        form = UserProfileInfoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/profile/')
        else:
            form = UserProfileInfoForm(instance=profile)
        context = {
             'form': form,
             'profile': profile
        }
        return render(request, 'accounts/edit_profile.html', context)




# We will not authenticate the user, instead we will sent an activation link
def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Check username
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,'That username is taken. Please try another!')
            return redirect('accounts:register')
        else:
            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR,'That email is already in use!')
                return redirect('accounts:register')
            else:
                # Looks good
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name
                                                )

                user.refresh_from_db()

                # A user is not considered to be active unless she/he has verified her/his email-id.
                user.is_active = False
                user.save()

                user.userprofile.first_name = request.POST.get('first_name')
                user.userprofile.last_name = request.POST.get('last_name')

                user.userprofile.save()

                # Send the account activation email
                current_site = get_current_site(request)
                subject = 'Please Activate Your Account'

                email_temp_name = 'accounts/activation_request.html'
                email_from = settings.DEFAULT_FROM_EMAIL
                context = {
                    'user': user,
                    'domain': current_site.domain,
                    'protocol': 'https' if request.is_secure() else 'http',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
                subject = ''.join(subject.splitlines())
                email = render_to_string(email_temp_name, context)
                html_message = email
                user.email_user(subject,  html_message, email_from, fail_silently=True)
                return render(request, 'accounts/account_activation_sent.html')
                
                # Log the user in and redirect to home page
                # login(request, user)
                # return redirect('index')
    else:
        return render(request, 'accounts/register.html')


def _login(request):
    # if request.user.is_authenticated:
    #     return redirect('accounts:get_user_profile', username=request.user.username)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in !')
            return redirect('feed:index')
        else:
            messages.error(request, "Hmm, wrong username or password. Please try again.")
            return redirect('accounts:_login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.INFO, 'You are logged out!')
    # return redirect('feed:index')
    return redirect('accounts:_login')


# Sent activation link
def activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


# def forgot_password(request):
#     if request.method == 'POST':
#         return password_reset(request, 
#             from_email=request.POST.get('email'))
#     else:
#         return render(request, 'accounts/password_reset.html')


# Activate user creating account
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid
    if user is not None and account_activation_token.check_token(user, token):
        """if valid, set active true"""
        user.is_active = True
        user.save()

        # Log the user in and redirect to home page
        login(request, user)
        # return redirect('index')
        messages.success(request,  'Your account has been successfully activated!')
        return redirect('/')
        # return redirect('accounts:activation_complete')
    else:
        return HttpResponse('Link Expired!')


# Setting view
@login_required
def account_settings(request):
    user = get_object_or_404(User, pk=request.user.id)
    if request.method == 'POST':
        setform = SettingForm(request.POST, instance=user.profile)
        if setform.is_valid():
            setform.save()
            messages.add_message(request, messages.INFO, 'Settings Saved.')
            return redirect(reverse('accounts:settings'))
    else:
        setform = SettingForm(instance=user.profile)
    return render(request, 'accounts/settings.html', {'form':setform})



# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = UserProfileInfoForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile was successfully updated')



# Sent password reset link
def password_reset_sent(request):
    return render(request, 'registration/password_reset_sent.html')


# password reset request
def password_reset_request(request):
    if request.method == 'POST':
        pw_reset_form = PasswordResetForm(request.POST)
        if pw_reset_form.is_valid:
            data = pw_reset_form.cleaned_data['email']
            ass_users = User.objects.filter(email=data, username=data)
            if ass_users.exists():
                current_site = get_current_site(request)
                subject = 'Password Reset Requested'
                email_temp_name = 'registration/password_reset_email.html'
                email_from = settings.DEFAULT_FROM_EMAIL

                context = {
                    'user': user,
                    'email': user.email,
                    'domain': current_site.domain,
                    'protocol': 'https' if request.is_secure() else 'http',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                }

                subject = ''.join(subject.splitlines())
                email = render_to_string(email_temp_name, context)
                html_message = email
                user.email_user(subject, html_message, email_from, fail_silently=False)

                return render(request, 'registration/password_reset_done.html')
    else:
        return render(request, 'registration/password_reset_form.html')


#user following method
def follow(request, username):
    user_to_follow = get_object_or_404(User, username = username)
    user = request.user
    data = {}
    print(user_to_follow)
    print(user)
    #chek if user already follow the user to follow
    followed = FollowUser.objects.filter(user = user, from_user = user_to_follow)
    is_followed = True if followed else False

    if is_followed:
        FollowUser.unfollow(user, user_to_follow)
        data['message'] = "You are already following this user."
        is_followed = False
    else:
        FollowUser.follow(user, user_to_follow)
        data['message'] = "You are now following {}".format(user_to_follow)
        is_followed = True

    resp = {
       "followed": is_followed,
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")
    # return HttpResponseRedirect(redirect_url)

# def follow_user(request, pk):
#     user_to_follow = get_object_or_404(User, pk=pk)
#     user_profile = request.user.userprofile
#     data = {}
#     if user_to_follow.to_user.filter(id=user_profile.id).exists():
#         data['message'] = "You are already following this user."
#     else:
#         user_to_follow.to_user.add(user_profile)
#         data['message'] = "You are now following {}".format(user_to_follow)
#     return JsonResponse(data, safe=False)


# Relationship request method
@login_required
def relationship_request(request):
    results = {'result': 'Fail'}
    if request.method == 'GET':
        obj = request.GET
        if 'request_type' in obj:
            if obj['request_type'] == 'send':
                # save user request to database
                from_user = User.objects.get(id=int(obj['from_user_id']))
                to_user = User.objects.get(id=int(obj['to_user_id']))
                message = obj['message']
                request = RelationshipRequest(from_user=from_user,
                                              to_user=to_user,
                                              message=message)
                request.save()

                # jeson response
                results = {'result': 'Request sent successfully'}

                # update topic table
                t = Topic()
                t.update_topic(from_user, 1, to_user)

            elif obj['request_type'] == 'accept':
                
                from_user = User.objects.get(id=int(obj['from_user_id']))
                to_user = User.objects.get(id=int(obj['to_user_id']))
                relation_type = RelationshipType.objects.get(name='Friend')
                relationship = Relationship(from_user=from_user,
                                            to_user=to_user,
                                            relation_type=relation_type)
                # save data in relationship table
                relationship.save()

                # getting relationship and accept
                request = RelationshipRequest.objects.get(from_user=from_user, to_user=to_user)
                request.delete()

                # json response
                results = {'result': 'Accepted!'}

                # update topic
                t = Topic()
                t.update_topic(to_user, 2, to_user)