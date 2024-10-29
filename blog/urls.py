## blog/urls.py
## description: the app-specific URLS for the blog application

from django.urls import path
from .views import ShowAllView, RandomArticleView, ArticlePageView, CreateCommentView, CreateArticleView, UpdateArticleView, DeleteCommentView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # map the URL (empty string) to the view
    # path(url, view, name)
    path('', RandomArticleView.as_view(), name='random'), 
    path('show_all', ShowAllView.as_view(), name='show_all'), 
    path('article/<int:pk>', ArticlePageView.as_view(), name='article'),
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'),
    path('create_article', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"),
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'),
    
    # authentication views
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'), ## NEW
]
