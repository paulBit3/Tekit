"""URL patterns for accounts app"""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    # user profile
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profiledetails/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('editprofile/<str:username>', views.edit_profile, name='edit_profile'),
    path('settings/', views.account_settings, name='account_settings'),
    
    # authentication and authorization
    path('login', views._login, name='_login'),
    path('register', views.register, name='register'),
    path('sent/',  views.activation_sent, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('logout', views.logout, name='logout'),

    # password reset URLs
    # path('password-reset/', views.password_reset_request, name='password_reset'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name= 'accounts/password_reset.html'), 
        name='password_reset'),

]