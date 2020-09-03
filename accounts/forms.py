from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile
import datetime


class UserForm(UserCreationForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta():
		model = User
		fields = ('first_name', 'last_name')
		# fields = ('first_name', 'last_name', 'username', 'email', 'password')

# Using django Crispy Form to render the profile template
class UserProfileInfoForm(forms.ModelForm):

	"""change the widget for date field"""
	dob = forms.DateField(
		label='What is your birth date?',
		# change range of the year
		widget=forms.SelectDateWidget(years=range(1900, datetime.date.today().year+5), attrs={'class': 'datepicker form-control', 'data-date-format': 'YYYY/MM/DD', 'style': 'width: 33%; display: inline-block;'})
		)
	class Meta():
		model = UserProfile
		fields = ('first_name', 'last_name', 'about_me', 'picture', 'phone_no', 'dob', 'city', 'state', 'status')
		exclude = ('user',)
		
	helper = FormHelper()
	helper.form_class = 'form-group'
	helper.layout = Layout(
		Field('first_name', css_class='form-control form-rounded mt-2 mb-3', attrs={ 'style:' 'width: 33%; display: inline-block;'}),
		Field('last_name', css_class='form-control form-rounded mt-2 mb-3'),
		Field('about_me', rows='2', css_class='input-xlarge form-control form-rounded mt-2 mb-3 col-xs-7'),
		Field('picture', css_class='form-control mt-2 mb-3'),
		Field('phone_no', css_class='form-control form-rounded mt-2 mb-3', placeholder="Format: 555-555-5555", pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"),
		Field('dob', css_class='form-rounded datepicker'),
		Field('city', css_class='form-control form-rounded mt-2 mb-3'),
		Field('state', css_class='form-control form-rounded mt-2 mb-3'),
		Field('status', css_class='form-control form-rounded mt-2 mb-3'),
		)
	helper.add_input(Submit('submit', 'Update Profile', css_class='btn btn-primary btn-block rounded-pill'))
	# HTML('<strong>add_input</strong>')
	# helper.form_show_labels = False 
    
