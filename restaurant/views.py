## restaurant/views.py
# description: the logic to handle URL requests
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random
import random
from datetime import datetime, timedelta

# Create your views here.

ITEM_PRICES = {
    'Chow Mein': {'small': 5.00, 'medium': 7.00, 'large': 9.00},
    'Fried Rice': {'small': 4.50, 'medium': 6.50, 'large': 8.50},
    'White Steamed Rice': {'small': 3.00, 'medium': 4.50, 'large': 6.00},
    'Super Greens': {'small': 4.00, 'medium': 6.00, 'large': 8.00}
}

DAILY_SPECIALS = {
    'Sweet and Sour Chicken': 10.00,
    'Beef with Broccoli': 12.00,
    'Kung Pao Chicken': 11.50,
    'Shrimp Lo Mein': 13.00
}

def main(request):
    '''
    A function to respond to the /restaurant URL.
    This function will delegate work to an HTML template.
    '''
    # this template will present the response
    template_name = "restaurant/main.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'letter1' : chr(random.randint(65,90)), # a letter in the range A ... Z
        'letter2' : chr(random.randint(65,90)), # a letter in the range A ... Z
        'number' : random.randint(1,10), # a number in the range 1...10
    }

    # delegate response to the template:
    return render(request, template_name, context)

def order(request):
    '''Show the web page with the form.'''
    template_name = "restaurant/order.html"

    daily_special_name = random.choice(list(DAILY_SPECIALS.keys()))
    daily_special_price = DAILY_SPECIALS[daily_special_name]

    context = {
        'daily_special': daily_special_name,
        'daily_special_price': daily_special_price
    }

    return render(request, template_name, context)

def confirmation(request):
    '''Process the form submission, and generate a result.'''
    template_name = "restaurant/confirmation.html"

    if request.POST:
        menu_items = request.POST.getlist('menu_items')
        item_sizes = []
        total_price = 0
        
        for item in menu_items:
            size = request.POST.get(f'{item.replace(" ", "_")}_size', 'medium')
            price = ITEM_PRICES[item][size]
            item_sizes.append((item, size, price))
            total_price += price
            
        daily_special_name = request.POST.get('daily_special')
        daily_special_price = float(request.POST.get('daily_special_price'))

        if request.POST.get('daily_special_selected') == 'yes':
            item_sizes.append((daily_special_name, None, daily_special_price))
            total_price += daily_special_price

        special_instructions = request.POST.get('special_instructions', '')
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        
        random_minutes = random.randint(30, 60)
        ready_time = datetime.now() + timedelta(minutes=random_minutes)
        formatted_ready_time = ready_time.strftime('%I:%M %p')

        context = {
            'item_sizes': item_sizes,
            'special_instructions': special_instructions,
            'name': name,
            'phone': phone,
            'email': email,
            'ready_time': formatted_ready_time,
            'total_price': total_price
        }

    return render(request, template_name, context)