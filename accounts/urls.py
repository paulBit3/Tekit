"""URL patterns for accounts app"""

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    # user profile
    path('users/profile/<str:username>/', views.get_user_profile, name='get_user_profile'),
    path('users/profiledetails/<str:username>/', views.profile_detail, name='profile_detail'),
    path('users/editprofile/', views.edit_profile, name='edit_profile'),
    path('users/settings/', views.account_settings, name='account_settings'),
    
    # authentication and authorization
    path('login', views._login, name='_login'),
    path('register', views.register, name='register'),
    path('sent/',  views.activation_sent, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('logout', views.logout, name='logout'),

    # password reset URLs
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('accounts:password_reset_complete')
        ), name='password_reset_confirm'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('accounts:password_reset_done')
        ), name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name= 'registration/password_reset_done.html'), name='password_reset_done'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name= 'registration/password_reset_complete.html'), 
        name='password_reset_complete'),

    # password change URLs
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name= 'registration/password_change_done.html'), name='password_change_done'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name= 'registration/password_change_form.html',
        success_url=reverse_lazy('accounts:password_change_done')), 
        name='password_change'),
    

]