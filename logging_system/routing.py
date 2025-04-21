from django.urls import path, re_path
from .consumers import LSTConsumer, SerialConsumer

#: WebSocket URL patterns for Django Channels routing.
#:
#: Routes:
#: - "ws/lst/": WebSocket connection for Local Sidereal Time updates via `LSTConsumer`.

websocket_urlpatterns = [
    path("ws/lst/", LSTConsumer.as_asgi()),
    re_path(r'ws/serial/$', SerialConsumer.as_asgi()),  # WebSocket endpoints
]
