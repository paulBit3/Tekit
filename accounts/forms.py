from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile



class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username', 'email', 'first_name', 'password')


class UserProfileInfoForm(forms.ModelForm):
	class Meta():
		model = Profile
		fields = ('name', 'photo', 'phone', 'birthdate', 'city', 'state')
			
		