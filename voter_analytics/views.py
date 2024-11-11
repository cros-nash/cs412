# views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter

class VotersListView(ListView):
    '''View to display voter results'''
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset()
        
        party = self.request.GET.get('party')
        if party:
            qs = qs.filter(party=party)
        
        min_dob = self.request.GET.get('min_dob')
        if min_dob:
            qs = qs.filter(dob__gte=f'{min_dob}-01-01')
        
        max_dob = self.request.GET.get('max_dob')
        if max_dob:
            qs = qs.filter(dob__lte=f'{max_dob}-12-31')
        
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            qs = qs.filter(voter_score=voter_score)
        
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for election in elections:
            if self.request.GET.get(election):
                qs = qs.filter(**{election: 'TRUE'})
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['parties'] = Voter.objects.order_by('party').values_list('party', flat=True).distinct()
        context['voter_scores'] = Voter.objects.order_by('voter_score').values_list('voter_score', flat=True).distinct()
        years = Voter.objects.dates('dob', 'year')
        context['years'] = [year.year for year in years]
        context['elections'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        context['current_filters'] = self.request.GET
        
        params = self.request.GET.copy()
        
        if 'page' in params:
            del params['page']
        context['query_string'] = params.urlencode()
        
        return context

class VoterDetailView(DetailView):
    '''View to display a single voter's details'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'