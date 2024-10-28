## mini_fb/urls.py
## description: the app-specific URLS for the mini_fb application

from django.urls import path
from .views import DeleteStatusMessageView, ShowAllView, ShowFriendSuggestionsView, ShowProfileView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, UpdateStatusMessageView, CreateFriendView # our view class definition 

urlpatterns = [
    path('', ShowAllView.as_view(), name='show_all_profiles'), # generic class-based view
    path('profile/<int:pk>', ShowProfileView.as_view(), name='profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('profile/<int:pk>/add_friend/<int:other_pk>', CreateFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
]