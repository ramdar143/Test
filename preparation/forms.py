from django import forms
from .models import PrepTask, ScheduleSlot

class PrepTaskForm(forms.ModelForm):
    due_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = PrepTask
        fields = ['task_name', 'assigned_to', 'due_time', 'status', 'related_order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally add additional logic to modify fields or restrict options
        self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(role='KitchenStaff')

class ScheduleSlotForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = ScheduleSlot
        fields = ['start_time', 'end_time', 'staff', 'task']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = self.fields['staff'].queryset.filter(role__in=['KitchenStaff', 'DeliveryStaff'])


class PrepTaskStatusForm(forms.ModelForm):
    class Meta:
        model = PrepTask
        fields = ['status']  # Only allow status to be updated