from django import forms
from .models import PaymentMethod

class PaymentSelectionForm(forms.Form):
    METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('gcash', 'GCash'),
        ('cod', 'Cash on Delivery (COD)'),
    ]
    method = forms.ChoiceField(choices=METHOD_CHOICES, widget=forms.RadioSelect)

class PayPalPaymentForm(forms.Form):
    email_or_mobile = forms.CharField(
        label="Email or Mobile Number",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'paypal-input',
            'placeholder': 'Email or mobile number'
        })
    )

class GCashPaymentForm(forms.Form):
    phone_number = forms.CharField(label="GCash Phone Number", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(label="Amount", max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    gcash_code = forms.CharField(label="GCash Code", max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))