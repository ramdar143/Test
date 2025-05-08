from datetime import datetime
from django import forms
from .models import BulkOrder

class BulkOrderForm(forms.ModelForm):
    class Meta:
        model = BulkOrder
        fields = ['base_order', 'contract_terms', 'frequency', 'next_delivery_date']

    def clean_next_delivery_date(self):
        # Ensure the date is in the correct format
        next_delivery_date_str = self.cleaned_data['next_delivery_date']
        
        try:
            # If the date is in a string format, convert it to a datetime.date object
            return datetime.fromisoformat(next_delivery_date_str).date()
        except ValueError:
            raise forms.ValidationError("Incorrect date format, please use YYYY-MM-DD.")
