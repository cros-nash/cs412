## blog/views.py
# description: the logic to handle URL requests
#from django.shortcuts import render
from typing import Any
from django.urls import reverse
from .models import Article, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
import random

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'
    
class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        '''Return one Article object chosen at random.'''
        all_articles = Article.objects.all()
        return random.choice(all_articles)

class ArticlePageView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    
class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        
        # find the pk from the URL
        pk = self.kwargs['pk']
        
        # find the corresponding article
        article = Article.objects.get(pk=pk)
        
        # add article to context data
        context['article'] = article
        
        return context
    
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        article = Article.objects.get(pk=self.kwargs['pk'])
        # print(article)
        form.instance.article = article
        return super().form_valid(form)
    
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
    
class CreateArticleView(CreateView):
    '''A view to create a new Article and save it to the database.'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
        # delegate work to the superclass version of this method
        return super().form_valid(form)
    
class UpdateArticleView(UpdateView):
    '''A view to update article and save it to the database.'''
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"
    model = Article
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
        return super().form_valid(form)
    
    
class DeleteCommentView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''
    template_name = "blog/delete_comment_form.html"
    model = Comment
    context_object_name = 'comment'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the article to which this Comment is related by FK
        article = comment.article
        
        # reverse to show the article page
        return reverse('article', kwargs={'pk':article.pk})