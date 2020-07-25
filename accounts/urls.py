"""URL patterns for accounts app"""

from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # user profile
    path('profile/', views.userprofile, name='user_profile'),
    path('editprofile/', views.edit_profile, name='edit_profile'),
    
    # authentication and authorization
    path('login', views._login, name='_login'),
    path('register', views.register, name='register'),
    path('sent/',  views.activation_sent, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('logout', views.logout, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('reset/', views.password_reset_sent, name='password_reset_sent'),
]