from django.contrib import admin
from django.urls import path
from . import views

app_name = 'TODO'

urlpatterns = [
    path("", views.Home, name='home'),
    path('edit/<int:task_id>/', views.Create_EditTask, name='Edit_Task' ),
    path('create/', views.Create_EditTask, name='Create_Task' ),
    path('delete/<int:task_id>/', views.DeleteTask, name='Delete_Task' ),
    path('toggle/<int:task_id>/', views.toggle_task_status, name='toggle_task'),
]