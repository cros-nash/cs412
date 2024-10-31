from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from typing import Any
from .models import Image, Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all mini_fb profiles.'''
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        # Add 'current_time' to the context
        context['current_time'] = timezone.now()
        return context

class ShowProfileView(DetailView):
    '''Show the details for one profile.'''
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        # Add 'current_time' to the context
        context['current_time'] = timezone.now()
        return context
    
class CreateProfileView(LoginRequiredMixin, CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    
    def form_valid(self, form):
        self.object = form.save()
        print(self.object.pk)  # Debugging print statement
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting the form.'''
        # Redirect to the profile detail page using the newly created profile's pk
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the existing context
        context = super().get_context_data(**kwargs)
        # Add 'current_time' to the context
        context['current_time'] = timezone.now()
        return context
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        pk = self.kwargs['pk']
        
        profile = Profile.objects.get(pk=pk)
        
        context['profile'] = profile
        context['current_time'] = timezone.now()
        return context
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
    
    def form_valid(self, form):
        sm = form.save(commit=False)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        sm.profile = profile
        sm.save()
        print("StatusMessage saved:", sm)

        files = self.request.FILES.getlist('files')
        print("Uploaded files:", files)

        for file in files:
            print(f"Processing file: {file}")

            image = Image(
                status_message=sm,
                image_file=file
            )
            try:
                image.save()
                print(f"Image saved: {image}")
            except Exception as e:
                print(f"Error saving image: {e}")
        
        # Call the parent form_valid method to complete the process
        return super().form_valid(form)

    
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})
    
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        pk = self.kwargs['pk']
        
        profile = Profile.objects.get(pk=pk)
        
        context['profile'] = profile
        context['current_time'] = timezone.now()
        return context
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "message"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        profile = self.object.profile
        context['profile'] = profile
        context['current_time'] = timezone.now()
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully deleting status message.'''
        profile = self.object.profile
        return reverse('profile', kwargs={'pk': profile.pk})
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage 
    form_class = UpdateStatusMessageForm  
    template_name = "mini_fb/update_status_form.html" 
    context_object_name = "message" 

    def get_success_url(self):
        '''Return the URL to redirect to after successfully updating the status message.'''
        profile = self.object.profile 
        return reverse('profile', kwargs={'pk': profile.pk})

    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')

class CreateFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        other_pk = kwargs.get('other_pk')

        profile = get_object_or_404(Profile, id=pk)
        friend_profile = get_object_or_404(Profile, id=other_pk)

        profile.add_friend(friend_profile)

        return redirect('profile', pk=profile.pk)
    
    def get_login_url(self) -> str:
        '''Return the URL to the login page.'''
        return reverse('login')
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['news_feed'] = profile.get_news_feed()
        return context