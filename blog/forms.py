# blog/forms.py

from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        # fields = ['article', 'author', 'text', ]
        # remove the article because we want to do this auto-magically
        fields = ['author', 'text', ]