from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.conf import settings

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from .tokens import account_activation_token
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.

# We will not authenticate the user, instead we will sent an activation link
def register(request):
    if request.method == 'POST':
        first_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, 'That username is taken. Please try another')
            return redirect('accounts:register')
        else:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is already in used')
                return redirect('accounts:register')
            else:
                # Looks good
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                first_name=first_name
                                                )
                # A user is not considered to be active unless she/he has verified her/his email-id.
                user.is_active = False
                user.save()

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
                user.email_user(subject,  html_message, email_from)
                return render(request, 'accounts/account_activation_sent.html')

                # Log the user in and redirect to home page
                # login(request, user)
                # return redirect('index')
    else:
        return render(request, 'accounts/register.html')


def _login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in !')
            return redirect('feed:topics')
        else:
            messages.error(request, "Hmm, we don't recognize that credentials. Please try again.")
            return redirect('accounts:_login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out.')
    return redirect('feed:index')


def password_reset(request,):
    return

# Sent activation link
def activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')


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
        login(request, user)
        # return redirect('index')
        messages.success(request,  'Registration completed. Please login to your account. ')
        return redirect('accounts:_login')
        # return render(request, 'accounts/login.html')
    else:
        return HttpResponse('Activation link is inactive!')

# Update user profile
def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.photo