import os

from apps.business_game import routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application
from services.websockets.middlewares import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": OriginValidator(
            TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)), ["*"]
        ),
    }
)
