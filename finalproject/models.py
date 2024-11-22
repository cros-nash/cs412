from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='items/', null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_listed = models.DateTimeField(auto_now_add=True)
    quantity_available = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Cart'),
        ('shipped', 'Shipped')
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.TextField(choices=STATUS_CHOICES, default='cart')

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.title} in Order #{self.order.id}"
