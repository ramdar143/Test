from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class User(AbstractUser):

    class Roles(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        KITCHEN = 'KitchenStaff', 'Kitchen Staff'
        DELIVERY = 'DeliveryStaff', 'Delivery Staff'
        ORDER_MANAGER = 'OrderManager', 'Order Manager'
        CUSTOMER = 'Customer', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CUSTOMER
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'



