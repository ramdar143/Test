from django.db import models
from orders.models import Order

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="invoices")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15,
        choices=[
            ('Unpaid', 'Unpaid'),
            ('Paid', 'Paid'),
            ('Cancelled', 'Cancelled')
        ],
        default='Unpaid'
    )
    

    def __str__(self):
        return f"Invoice #{self.id} - Order {self.order.id}"