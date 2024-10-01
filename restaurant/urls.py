## restaurant/urls.py
## description: the app-specific URLS for the restaurant application

from django.urls import path
from django.conf import settings
from . import views

# create a list of URLs for this app:
urlpatterns = [
    path(r'', views.main, name="main"), 
    path(r'order', views.order, name="order"), ## new
    path(r'confirmation', views.confirmation, name="confirmation"), ## new
]

