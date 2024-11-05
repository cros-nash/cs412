from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from . models import Result

class ResultsListView(ListView):
    '''View to display marathon results'''
    template_name = 'marathon_analytics/results.html'
    model = Result
    context_object_name = 'results'
    paginate_by = 50
    def get_queryset(self):
        
        # start with entire queryset
        qs = super().get_queryset().order_by('place_overall')
        # filter results by these field(s):
        if 'first_name' in self.request.GET:
            first_name = self.request.GET['first_name']
            if first_name:
                qs = qs.filter(first_name=first_name)
                
        return qs