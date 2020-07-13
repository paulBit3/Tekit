from django import forms

from .models import Topic, Feed, Comment

class TopicForm(forms.ModelForm):
    def clean_topic_field(self):
        fields = self.cleaned_data['fields']
        return fields

    class Meta:
        model = Topic
        fields = ['text', 'image',]
        labels = {'text': ''}


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

    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': ''}
        widgets = {'comment': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Type your comment'})}