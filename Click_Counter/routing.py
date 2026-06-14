from django.urls import path
from .consumer import ClickerConsumer

websocket_urlpatterns = [
    path('ws/counter/', ClickerConsumer.as_asgi()),
]