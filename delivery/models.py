# delivery/models.py
from django.db import models
from users.models import User  # Assuming User model is in the 'users' app
from orders.models import Order  # Import Order model to link with deliveries

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Failed', 'Failed'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    assigned_driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'DeliveryStaff'})
    delivery_address = models.CharField(max_length=255)
    delivery_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Delivery for {self.order.customer_name} (Status: {self.status})"
