from django.contrib import admin
from .models import UserProfile, Category, Item, Order, OrderItem, Discount

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)