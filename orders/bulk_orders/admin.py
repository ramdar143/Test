from django.contrib import admin
from .models import BulkOrder

@admin.register(BulkOrder)
class BulkOrderAdmin(admin.ModelAdmin):
    list_display = ('base_order', 'frequency', 'next_delivery_date')
    list_filter = ('frequency',)
