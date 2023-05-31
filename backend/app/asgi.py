import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing
from app.middlewares import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),  # WSGI
        "websocket": JWTAuthMiddleware(URLRouter(chat.routing.websocket_urlpatterns)),  # ASGI
        # Just HTTP for now. (We can add other protocols later.)
    }
)