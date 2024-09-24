## hw/views.py
# description: the logic to handle URL requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

author_set = ['Galileo Galilei', 'Stefan Banach', 'Sofia Kovalevskaya', 'Edsger Dijkstra']

author_url = [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Galileo_Galilei_%281564-1642%29_RMG_BHC2700.tiff/lossy-page1-220px-Galileo_Galilei_%281564-1642%29_RMG_BHC2700.tiff.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Stefana_Banach_-_ستيفان_بناخ.jpg/200px-Stefana_Banach_-_ستيفان_بناخ.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Sofja_Wassiljewna_Kowalewskaja_1.jpg/220px-Sofja_Wassiljewna_Kowalewskaja_1.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Edsger_Wybe_Dijkstra.jpg/220px-Edsger_Wybe_Dijkstra.jpg',
]

author_quote = [
            'Nature is written in mathematical language.',
            'Mathematics is the most beautiful and most powerful creation of the human spirit.',
            'It is impossible to be a mathematician without being a poet in soul.',
            'Math is like going to the gym for your brain. It sharpens your mind.',
]

author_info = [
    "Galileo di Vincenzo Bonaiuti de' Galilei, commonly referred to as Galileo Galilei, was an Italian astronomer, physicist and engineer, sometimes described as a polymath. He was born in the city of Pisa, then part of the Duchy of Florence and present-day Italy.",
    "Stefan Banach was a Polish mathematician who is generally considered one of the 20th century's most important and influential mathematicians. He was the founder of modern functional analysis, and an original member of the Lwów School of Mathematics.",
    "Sofya Vasilyevna Kovalevskaya, born Korvin-Krukovskaya, was a Russian mathematician who made noteworthy contributions to analysis, partial differential equations and mechanics.",
    "Edsger Wybe Dijkstra was a Dutch computer scientist, programmer, software engineer, mathematician, and science essayist. Born in Rotterdam, the Netherlands, Dijkstra studied mathematics and physics and then theoretical physics at the University of Leiden."
]

def quote(request):
    '''
    A function to respond to the /quotes URL.
    This function will delegate work to an HTML template.
    '''
    # this template will present the response
    template_name = "quotes/quote.html"

    global number
    number = random.randint(1,4)

    context = {
        'current_time': time.ctime(),
        'number' : number, # a number in the range 1...10
        'author' : author_set[number - 1],
        'img_url' : author_url[number - 1],
        'quote' : author_quote[number - 1]
    }
    
    # delegate response to the template:
    return render(request, template_name, context)

def about(request):
    '''
    A function to respond to the /quotes/about URL.
    This function will delegate work to an HTML template.
    '''
    # this template will present the response
    template_name = "quotes/about.html"
    
    context = {
        'current_time': time.ctime(),
        'author' : author_set[number - 1],
        'info' : author_info[number - 1],
    }

    # delegate response to the template:
    return render(request, template_name, context)

def show_all(request):
    '''
    A function to respond to the /quotes/about URL.
    This function will delegate work to an HTML template.
    '''
    # this template will present the response
    template_name = "quotes/show_all.html"
    
    context = {
        'current_time': time.ctime(),
        'authors' : author_set,
        'images' : author_url,
        'quotes' : author_quote
    }

    # delegate response to the template:
    return render(request, template_name, context)