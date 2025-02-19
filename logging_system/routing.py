from django.urls import path
from .consumers import LSTConsumer

websocket_urlpatterns = [
    path("ws/lst/", LSTConsumer.as_asgi()),  # ✅ WebSocket endpoint
]
