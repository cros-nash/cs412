# blog/forms.py

from django import forms
from .models import Article, Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        # fields = ['article', 'author', 'text', ]
        # remove the article because we want to do this auto-magically
        fields = ['author', 'text', ]
        
class CreateArticleForm(forms.ModelForm):
    '''A form to add a new Article to the database.'''
    class Meta:
        '''Associate this form with the Article model; select fields to add.'''
        model = Article
        fields = ['author', 'title', 'text', 'image_file']
        
class UpdateArticleForm(forms.ModelForm):
    '''A form to update a quote to the database.'''
    class Meta:
        '''associate this form with the Article model.'''
        model = Article
        fields = ['title', 'text', ]  # which fields from model should we use