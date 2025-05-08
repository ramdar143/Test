from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PrepTask
from .forms import PrepTaskForm  # Assuming you have a form to edit PrepTask
from django.views.generic import ListView
from .models import PrepTask, ScheduleSlot
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import PrepTask, ScheduleSlot
from .forms import PrepTaskForm, ScheduleSlotForm
from django.utils import timezone  
from orders.models import Order

@login_required
def view_prep_tasks(request):
    tasks = PrepTask.objects.filter(assigned_to=request.user)
    now = timezone.now()
    for task in tasks:
        task.is_overdue = task.due_time and (task.due_time < now) and (task.status != 'Done')
    return render(request, 'prep_tasks/view_tasks.html', {'prep_tasks': tasks})


from .forms import PrepTaskStatusForm
@login_required
def update_prep_task(request, pk):
    task = get_object_or_404(PrepTask, pk=pk, assigned_to=request.user)

    if request.method == 'POST':
        form = PrepTaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('users:kitchen_dashboard')
    else:
        form = PrepTaskStatusForm(instance=task)

    return render(request, 'preparation/prep_task_form.html', {'form': form, 'task': task})


@login_required
def kitchen_task_list(request):
    tasks = PrepTask.objects.filter(assigned_to=request.user)
    return render(request, 'preparation/kitchen_task_list.html', {'tasks': tasks})


@login_required
def kitchen_task_detail(request, pk):
    task = get_object_or_404(PrepTask, pk=pk, assigned_to=request.user)
    return render(request, 'preparation/kitchen_task_detail.html', {'task': task})


# List View for PrepTasks
class PrepTaskListView(ListView):
    model = PrepTask
    template_name = 'preparation/prep_task_list.html'
    context_object_name = 'prep_tasks'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        for task in context['prep_tasks']:
            task.is_overdue = task.due_time and (task.due_time < now) and (task.status != 'Done')
        return context

# Create View for PrepTask
class PrepTaskCreateView(CreateView):
    model = PrepTask
    form_class = PrepTaskForm
    template_name = 'preparation/prep_task_form.html'
    success_url = reverse_lazy('preparation:prep_task_changelist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Show all active/incomplete orders as candidates
        context['related_orders'] = Order.objects.exclude(status='Completed').order_by('-created_at')
        return context

# Update View for PrepTask
class PrepTaskUpdateView(UpdateView):
    model = PrepTask
    form_class = PrepTaskForm
    template_name = 'preparation/prep_task_form.html'
    success_url = reverse_lazy('preparation:prep_task_changelist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Show all active/incomplete orders as candidates
        context['related_orders'] = Order.objects.exclude(status='Completed').order_by('-created_at')
        return context

# Delete View for PrepTask
class PrepTaskDeleteView(DeleteView):
    model = PrepTask
    template_name = 'preparation/confirm_delete.html'
    success_url = reverse_lazy('preparation:prep_task_changelist')

# List View for ScheduleSlots
class ScheduleSlotListView(ListView):
    model = ScheduleSlot
    template_name = 'preparation/schedule_slot_list.html'
    context_object_name = 'schedule_slots'

# Create View for ScheduleSlot
class ScheduleSlotCreateView(CreateView):
    model = ScheduleSlot
    form_class = ScheduleSlotForm
    template_name = 'preparation/schedule_slot_form.html'
    success_url = reverse_lazy('preparation:schedule_slot_changelist')

# Update View for ScheduleSlot
class ScheduleSlotUpdateView(UpdateView):
    model = ScheduleSlot
    form_class = ScheduleSlotForm
    template_name = 'preparation/schedule_slot_form.html'
    success_url = reverse_lazy('preparation:schedule_slot_changelist')

# Delete View for ScheduleSlot
class ScheduleSlotDeleteView(DeleteView):
    model = ScheduleSlot
    template_name = 'preparation/confirm_delete.html'
    success_url = reverse_lazy('preparation:schedule_slot_changelist')