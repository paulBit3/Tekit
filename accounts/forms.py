from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile
import datetime


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('username', 'email', 'first_name','last_name', 'password')
		


class UserProfileInfoForm(forms.ModelForm):
	"""change the widget for date field"""
	birthdate = forms.DateField(
		label='What is your birth date?',
		# change range of the year
		widget=forms.SelectDateWidget(years=range(1980, datetime.date.today().year-5))
		)
	class Meta():
		model = UserProfile
		fields = ('name', 'picture', 'phone_no', 'birthdate', 'city', 'state')
		exclude = ('user',)

class SettingForm(forms.ModelForm):
	"""A class for  Setting form"""

	class Meta:
		model = UserProfile
		fields = ('default_language', 'default_expiration' , 'default_exposure' , 'private')
		widgets = {
            'default_language': forms.Select(attrs={'class': 'selectpicker foo form-control',
                                                    'data-live-search': 'true',
                                                    'data-size': '5'}),
            'default_expiration': forms.Select(attrs={'class': 'selectpicker form-control'}),
            'default_exposure': forms.Select(attrs={'class': 'selectpicker form-control'})

        }
			
		