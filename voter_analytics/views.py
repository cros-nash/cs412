# views.py

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.functions import ExtractYear
from django.db import models
from .models import Voter
import plotly
import plotly.graph_objs as go

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
        context['years'] = sorted([year.year for year in years])
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
    
class GraphsView(ListView):
    '''View to display graphs of voter data'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'
    
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
        voters = context['voters']
        
        context['parties'] = Voter.objects.order_by('party').values_list('party', flat=True).distinct()
        context['voter_scores'] = Voter.objects.order_by('voter_score').values_list('voter_score', flat=True).distinct()
        years = Voter.objects.dates('dob', 'year')
        context['years'] = sorted([year.year for year in years])
        context['elections'] = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        context['current_filters'] = self.request.GET

        # Voter Score Distribution
        score_counts = voters.values('voter_score').annotate(count=models.Count('voter_score')).order_by('voter_score')
        scores = [entry['voter_score'] for entry in score_counts]
        score_counts = [entry['count'] for entry in score_counts]

        fig = go.Bar(x=scores, y=score_counts)
        graph_div_score = plotly.offline.plot(
            {"data": [fig], "layout": go.Layout(title="Voter Score Distribution", xaxis_title="Voter Score", yaxis_title="Count")},
            auto_open=False,
            output_type="div"
        )
        context['graph_div_score'] = graph_div_score
        
        # Voter Distribution by Year of Birth
        voter_years = voters.annotate(year_of_birth=ExtractYear('dob'))
        votes_per_year = voter_years.values('year_of_birth').annotate(count=models.Count('id')).order_by('year_of_birth')
        
        years = [entry['year_of_birth'] for entry in votes_per_year]
        year_counts = [entry['count'] for entry in votes_per_year]
        
        fig2 = go.Bar(x=years, y=year_counts)
        graph_div_birth_year = plotly.offline.plot(
            {
                "data": [fig2],
                "layout": go.Layout(
                    title="Distribution of Voters by Year of Birth",
                    xaxis_title="Year of Birth",
                    yaxis_title="Number of Voters"
                )
            },
            auto_open=False,
            output_type="div"
        )
        context['graph_div_birth_year'] = graph_div_birth_year
        
        # Voter Count by Election
        elections = [
            ('v20state', '2020 State Election'),
            ('v21town', '2021 Town Election'),
            ('v21primary', '2021 Primary Election'),
            ('v22general', '2022 General Election'),
            ('v23town', '2023 Town Election'),
        ]

        election_labels = []
        voter_counts = []

        for election, label in elections:
            count_voted = voters.filter(**{election: 'TRUE'}).count()
            election_labels.append(label)
            voter_counts.append(count_voted)

        fig3 = go.Bar(x=election_labels, y=voter_counts)
        graph_div_elections = plotly.offline.plot(
            {
                "data": [fig3],
                "layout": go.Layout(
                    title="Voter Participation in Elections",
                    xaxis_title="Election",
                    yaxis_title="Number of Voters Who Voted"
                )
            },
            auto_open=False,
            output_type="div"
        )

        context['graph_div_elections'] = graph_div_elections

        return context