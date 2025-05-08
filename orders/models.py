from django.db import models
from django.conf import settings
from menu.models import MenuItem

class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        IN_PROGRESS = 'In Progress', 'In Progress'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'

    class EventType(models.TextChoices):
        WEDDING = 'Wedding', 'Wedding'
        BIRTHDAY = 'Birthday', 'Birthday'
        CORPORATE = 'Corporate', 'Corporate'
        OTHER = 'Other', 'Other'

    class PaymentStatus(models.TextChoices):
        NOT_PAID = 'Not Paid', 'Not Paid'
        PAID = 'Paid', 'Paid'
        REFUNDED = 'Refunded', 'Refunded'
        DISPUTED = 'Disputed', 'Disputed'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    customer_contact = models.CharField(max_length=255)
    event_date = models.DateField()
    event_type = models.CharField(
        max_length=20,
        choices=EventType.choices,
        default=EventType.OTHER
    )
    guest_count = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    payment_status = models.CharField(
        max_length=15,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_PAID
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.customer.username} ({self.status})"

    def get_total(self):
        return sum(item.menu_item.price * item.quantity for item in self.items.all())

    @property
    def total(self):
        return self.get_total()

    def check_and_update_completion(self):
        # Import inside the method to avoid circular imports
        from preparation.models import PrepTask

        tasks = PrepTask.objects.filter(related_order=self)
        if tasks.exists() and all([task.status == PrepTask.Status.DONE for task in tasks]):
            self.status = Order.Status.COMPLETED
            self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity} (Order #{self.order.id})"