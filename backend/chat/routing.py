from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('api/ws/chat/<int:room_id>/', ChatConsumer.as_asgi()),
]
