
"""
ASGI configuration for Telescope Logging project.

This setup supports both:
- HTTP requests (via Django)
- WebSocket connections (via Channels and LSTConsumer)

Includes:
- ASGI app initialization with Django settings
- WebSocket routing using `ProtocolTypeRouter`
- Optional support for static file handling via WhiteNoise (if enabled elsewhere)
"""

import os
from pathlib import Path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from whitenoise import WhiteNoise
from logging_system.routing import websocket_urlpatterns

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Set the default settings module for the 'django' program
# This allows Django to find the settings file for the project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telescope_log.settings')

# Initialize the ASGI application for Django
# This is the entry point for ASGI-compatible web servers to serve your project.
django_asgi_app = get_asgi_application()


# ASGI application with both HTTP and WebSocket support
# (if you have static files configured in your settings)
application = ProtocolTypeRouter({
    "http": get_asgi_application(), # HTTP requests handled by Django
    "websocket": URLRouter(websocket_urlpatterns),  # WebSocket routing for LST updates

    # Add your websocket routing here if needed
})

