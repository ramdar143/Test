from django.db import models
from orders.models import Order

class BulkOrder(models.Model):
    class Frequency(models.TextChoices):
        WEEKLY = 'Weekly', 'Weekly'
        MONTHLY = 'Monthly', 'Monthly'
        CUSTOM = 'Custom', 'Custom'

    # Link to a standard order as a "template" or reference
    base_order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='bulk_details')

    contract_terms = models.TextField()
    frequency = models.CharField(max_length=20, choices=Frequency.choices, default=Frequency.WEEKLY)
    next_delivery_date = models.DateField()

    def __str__(self):
        return f"Bulk Order for {self.base_order.customer_name} - {self.frequency}"
