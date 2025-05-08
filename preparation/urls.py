# preparation/urls.py
from django.urls import path
from . import views

app_name = 'preparation'

urlpatterns = [
    path('prep-tasks/', views.PrepTaskListView.as_view(), name='prep_task_changelist'),
    path('prep-task/create/', views.PrepTaskCreateView.as_view(), name='prep_task_create'),
    path('prep-task/<int:pk>/edit/', views.PrepTaskUpdateView.as_view(), name='prep_task_edit'),
    path('prep-task/<int:pk>/delete/', views.PrepTaskDeleteView.as_view(), name='prep_task_delete'),
    path('schedule-slots/', views.ScheduleSlotListView.as_view(), name='schedule_slot_changelist'),
    path('schedule-slot/create/', views.ScheduleSlotCreateView.as_view(), name='schedule_slot_create'),
    path('schedule-slot/<int:pk>/edit/', views.ScheduleSlotUpdateView.as_view(), name='schedule_slot_edit'),
    path('schedule-slot/<int:pk>/delete/', views.ScheduleSlotDeleteView.as_view(), name='schedule_slot_delete'),
    path('prep-task/<int:pk>/update/', views.update_prep_task, name='prep_task_update'),
    path('my-tasks/', views.kitchen_task_list, name='kitchen_task_list'),
    path('my-tasks/<int:pk>/', views.kitchen_task_detail, name='kitchen_task_detail'),

]
