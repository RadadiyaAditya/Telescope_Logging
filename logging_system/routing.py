from django.urls import path
from .consumers import LSTConsumer

#: WebSocket URL patterns for Django Channels routing.
#:
#: Routes:
#: - "ws/lst/": WebSocket connection for Local Sidereal Time updates via `LSTConsumer`.

websocket_urlpatterns = [
    path("ws/lst/", LSTConsumer.as_asgi()),  # ✅ WebSocket endpoint
]
