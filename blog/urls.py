## blog/urls.py
## description: the app-specific URLS for the blog application

from django.urls import path
from .views import ShowAllView, RandomArticleView, ArticlePageView, CreateCommentView

urlpatterns = [
    # map the URL (empty string) to the view
    # path(url, view, name)
    path('', RandomArticleView.as_view(), name='random'), 
    path('show_all', ShowAllView.as_view(), name='show_all'), 
    path('article/<int:pk>', ArticlePageView.as_view(), name='article'),
    path('create_comment', CreateCommentView.as_view(), name='create_comment')
]
