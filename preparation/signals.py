# In preparation/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PrepTask

@receiver(post_save, sender=PrepTask)
def update_order_status_on_prep_completion(sender, instance, **kwargs):
    if instance.related_order:
        instance.related_order.check_and_update_completion()