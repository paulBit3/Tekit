from django import forms

from .models import *

# class TopicForm(forms.ModelForm):
#     def clean_topic_field(self):
#         fields = self.cleaned_data['fields']
#         return fields

#     class Meta:
#         model = TopicAction
#         fields = ['name', 'image',]
#         labels = {'name': ''}
#         widgets = {'name': forms.TextInput(
#             attrs={'rows': 4, 'cols': 40, 'placeholder': 'Type your topic here'})}



class FeedForm(forms.ModelForm):
    def clean_post_field(self):
        fields = self.cleaned_data['fields']
        return fields

    class Meta:
        model = Feed
        fields = ['text', 'image',]
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Type your feed here'})}


class CommentForm(forms.ModelForm):
    """docstring for CommentForm"""
    def clean_comment_field(self):
        fields = self.cleaned_data['fields']
        return fields

    # this function will be used for the validation
    # def clean(self):
    #     #data from the form is fetched using super function 
    #     super(CommentForm, self).clean()
    #     fields = self.cleaned_data['fields']

    #     if len(fields) < 25:
    #         self._errors['fields'] = self.error_class([
    #             'Comment should contain a minimum of 25 characters'])
    #     #return any errors if found 
    #     return self.cleaned_data 

    class Meta:
        model = Comment
        fields = ['content']
        # labels = {'comment': ''}
        widgets = {'comment': forms.Textarea(attrs={'rows': '2', 'cols': '25', 'placeholder': 'Type your comment'})}


class SettingForm(forms.ModelForm):
    """docstring for SettingForm"""
    def __init__(self, arg):
        super(SettingForm, self).__init__()
        self.arg = arg

    class Meta:
        model = UserProfile
        fields = ['name', 'about_me', 'picture', 'phone_no', 'birthdate', 'city', 'state', 'status']
        widgets = {'class': ' form-control'}
        