import os
from pathlib import Path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from whitenoise import WhiteNoise
from logging_system.routing import websocket_urlpatterns

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telescope_log.settings')

django_asgi_app = get_asgi_application()

django_asgi_app = WhiteNoise(django_asgi_app, root=str(BASE_DIR / 'staticfiles'))

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(websocket_urlpatterns),  # ✅ Add WebSocket support

    # Add your websocket routing here if needed
})

