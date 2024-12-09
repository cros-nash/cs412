# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Item, UserProfile, OrderItem

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    address = forms.CharField(widget=forms.TextInput, label='Address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match.")
        return password_confirm

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'image', 'category', 'quantity_available']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='Quantity',
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 100px; display: inline-block; margin-right: 10px;',
            'placeholder': '1',
        })
    )

class UpdateQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='Quantity',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;',
        })
    )
