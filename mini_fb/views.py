from django.utils import timezone
from django.views.generic import ListView
from .models import Profile

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
