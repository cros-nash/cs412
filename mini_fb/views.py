from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from typing import Any
from .models import Profile
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse

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
    
class CreateProfileView(CreateView):
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
class CreateStatusMessageView(CreateView):
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
    
    def form_valid(self, form):
        print(form.cleaned_data)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # print(article)
        form.instance.profile = profile
        return super().form_valid(form)
    
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})