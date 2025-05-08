from django.contrib import admin
from .models import PaymentMethod, Invoice

admin.site.register(PaymentMethod)
admin.site.register(Invoice)