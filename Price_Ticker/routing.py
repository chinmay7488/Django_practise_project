from django.urls import path
from .consumer import TickerConsumer

websocket_urlpatterns = [
    path('ws/dashboard/', TickerConsumer.as_asgi()),
]