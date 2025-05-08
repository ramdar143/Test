# admin.py

from django.contrib import admin
from .models import PrepTask, ScheduleSlot

class PrepTaskAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'status', 'assigned_to', 'due_time', 'related_order']
    list_filter = ['status', 'assigned_to']
    search_fields = ['task_name', 'assigned_to__username']

class ScheduleSlotAdmin(admin.ModelAdmin):
    list_display = ['staff', 'task', 'start_time', 'end_time']
    list_filter = ['staff', 'task']
    search_fields = ['staff__username', 'task__task_name']

admin.site.register(PrepTask, PrepTaskAdmin)
admin.site.register(ScheduleSlot, ScheduleSlotAdmin)
