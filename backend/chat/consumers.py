import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser

from .models import Room, Message
from channels.exceptions import DenyConnection


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = 'chat_%s' % self.room_id

        user = self.scope.get('user', None)

        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

        if isinstance(self.scope['user'], AnonymousUser):
            print('User is Anonymous: ', self.scope['user'])
            raise DenyConnection(4001)
            await self.close(code=4001)
        else:
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        try:
            print("Data Received: ", text_data)
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']

            # Save message to database
            room = await sync_to_async(Room.objects.get_or_create)(id=self.room_id)
            message = await sync_to_async(Message.objects.create)(room=room, username=username, text=message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_id,
                {
                    'type': 'chat_message',
                    'message': message.text,
                    'username': message.username,
                    'timestamp': message.timestamp.isoformat()
                }
            )
        except json.JSONDecodeError:
            print('Invalid JSON: ', text_data)

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))
