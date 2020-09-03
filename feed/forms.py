from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field

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
       
    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.layout = Layout(
        Field('text',rows="2", css_class='input-xlarge form-control form-rounded mt-2 mb-3 col-xs-7 '),
        Field('image'),
        )
    helper.add_input(Submit('submit', 'Post Feed', css_class='btn btn-primary rounded-pill'))


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
        widgets = {'comment': forms.Textarea(
            attrs={'rows': '2', 
                   'cols': '8', 
                   'placeholder': 'Say something...', 
                   'class': 'form-control'
                   })
        }

class ReplyForm(forms.ModelForm):
    """docstring for CommentForm"""
    def clean_reply_field(self):
        fields = self.cleaned_data['fields']
        return fields

    class Meta:
        model = Reply
        fields = ['content']
        # labels = {'reply': ''}
        widgets = {'reply': forms.Textarea(
            attrs={'rows': '2', 
                   'cols': '8', 
                   'placeholder': 'Replying...', 
                   'class': 'form-control'
                   })
        }
