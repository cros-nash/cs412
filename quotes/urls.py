## quotes/urls.py
## description: the app-specific URLS for the quotes application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    path(r'', views.quote, name="home"), 
    path(r'about', views.about, name="about"), ## new
    path(r'show_all', views.show_all, name="show_all"), ## new
]

