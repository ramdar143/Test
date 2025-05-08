# payments/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from .models import Invoice

@receiver(post_save, sender=Order)
def create_invoice_after_payment(sender, instance, **kwargs):
    if instance.payment_status == Order.PaymentStatus.PAID:
        if not Invoice.objects.filter(order=instance, status='Paid').exists():
            Invoice.objects.create(
                order=instance,
                amount=instance.total,
                status='Paid'
            )