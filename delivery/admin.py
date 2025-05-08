from django.contrib import admin
from .models import Delivery

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'assigned_driver', 'delivery_time', 'status')
    list_filter = ('status', 'delivery_time')
    search_fields = ('tracking_number',)
