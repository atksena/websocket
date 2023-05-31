from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer
import asyncio
from channels.consumer import AsyncConsumer


class PostBodyViewSet(ModelViewSet):
    def get_object(self):
        """
        Overridden to work with POST body instead of url variable.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.data.get(self.lookup_field)}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj


class RoomViewSet(PostBodyViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MessageViewSet(PostBodyViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
