from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
def home(request):
    '''
    A function to respond to the /hw URL.
    This function will delegate work to an HTML template.
    '''
    # this template will present the response
    template_name = "hw/home.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'letter1' : chr(random.randint(65,90)), # a letter in the range A ... Z
        'letter2' : chr(random.randint(65,90)), # a letter in the range A ... Z
        'number' : random.randint(1,10), # a number in the range 1...10
    }

    # delegate response to the template:
    return render(request, template_name, context)