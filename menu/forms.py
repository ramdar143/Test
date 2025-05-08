# menu/forms.py
from django import forms
from .models import Category, MenuItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'is_available', 'allergens', 'image']
