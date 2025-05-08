from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Allergen(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    allergens = models.ManyToManyField(Allergen, blank=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)  # Add this line for image

    def __str__(self):
        return self.name
