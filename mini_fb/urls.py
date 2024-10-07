## mini_fb/urls.py
## description: the app-specific URLS for the mini_fb application

from django.urls import path
from .views import ShowAllView # our view class definition 

urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all_profiles'), # generic class-based view
]