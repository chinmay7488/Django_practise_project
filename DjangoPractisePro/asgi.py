import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoPractisePro.settings")
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import Price_Ticker.routing
import Click_Counter.routing
import Chat_Room.routing


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        Price_Ticker.routing.websocket_urlpatterns + 
        Click_Counter.routing.websocket_urlpatterns + 
        Chat_Room.routing.websocket_urlpatterns
    ),
})
