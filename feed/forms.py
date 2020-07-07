from django import forms

from .models import Topic, Feed

class TopicForm(forms.ModelForm):
    def clean_topic_field(self):
        fields = self.cleaned_data['fields']
        return fields

    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}


class FeedForm(forms.ModelForm):
    def clean_post_field(self):
        fields = self.cleaned_data['fields']
        return fields

    class Meta:
        model = Feed
        fields = ['text', 'image',]
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'placeholder': 'Tell your Tech history'})}


class CommentForm(forms.ModelForm):
    """docstring for CommentFomr"""
    class Meta:
        model = Comment
        fields = ('text')
            
        