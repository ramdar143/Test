from django.db import models
from django.conf import settings
from orders.models import Order

class PrepTask(models.Model):
    class Status(models.TextChoices):
        TODO = 'To Do', 'To Do'
        IN_PROGRESS = 'In Progress', 'In Progress'
        DONE = 'Done', 'Done'

    task_name = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'KitchenStaff'},
        related_name='prep_tasks'
    )
    due_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    related_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.task_name} ({self.status})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving, update associated order status if needed
        if self.related_order:
            self.related_order.check_and_update_completion()


class ScheduleSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['KitchenStaff', 'DeliveryStaff']}
    )
    task = models.ForeignKey(PrepTask, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.staff} - {self.task.task_name} [{self.start_time} - {self.end_time}]"
