from django.utils import timezone
from decimal import Decimal
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
    
class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)

    def is_valid(self):
        if not self.active:
            return False
        if self.expiration_date and timezone.now() > self.expiration_date:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        return True

    def __str__(self):
        return self.code


class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'Cart'),
        ('shipped', 'Shipped')
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.TextField(choices=STATUS_CHOICES, default='cart')

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"

    def calculate_total(self):
        total = sum(item.item.price * item.quantity for item in self.orderitem_set.all())
        if self.discount and self.discount.is_valid():
            if self.discount.discount_type == 'percentage':
                self.discount_amount = (self.discount.amount / 100) * total
            elif self.discount.discount_type == 'fixed':
                self.discount_amount = self.discount.amount
            total -= self.discount_amount
            if total < 0:
                total = 0
        else:
            self.discount_amount = 0.0
        self.total_amount = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.title} in Order #{self.order.id}"
    
    def total_price(self):
        return self.item.price * self.quantity

