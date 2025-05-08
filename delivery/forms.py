# delivery/forms.py

from django import forms
from .models import Delivery
from django.forms.widgets import DateTimeInput

class DeliveryForm(forms.ModelForm):
    delivery_time = forms.DateTimeField(
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],  # Matches HTML datetime-local format
    )

    class Meta:
        model = Delivery
        fields = ['delivery_person', 'delivery_time', 'status']
