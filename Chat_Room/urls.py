from django.urls import path
from . import views

app_name = 'Chat_Room'

urlpatterns = [
    path('', views.chat, name='chat'),
]
