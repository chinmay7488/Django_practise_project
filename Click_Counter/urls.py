from django.urls import path
from . import views

app_name = 'Click_Counter'

urlpatterns = [
    path('', views.counter, name='counter'),
]
