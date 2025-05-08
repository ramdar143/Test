# orders/forms.py
from django import forms
from .models import Order, OrderItem
from django.forms import inlineformset_factory


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_contact', 'event_date', 'event_type', 'guest_count']  # Removed 'customer' and 'status'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_date'].widget = forms.DateInput(attrs={'type': 'date'})

    def save(self, commit=True, user=None):
        order = super().save(commit=False)
        if user:
            order.customer = user  # Automatically set customer
        order.status = Order.Status.PENDING  # Default status
        if commit:
            order.save()
        return order


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'cols': 30,
                'style': 'resize: vertical; width: 100%;',
                'placeholder': 'Add notes (optional)...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].initial = 1  # Default quantity to 1 if not specified

# Formset for inline form handling
OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    form=OrderItemForm,
    fields=['menu_item', 'quantity', 'notes'],
    extra=1,  # Adjust this to control how many empty forms to show initially
)
