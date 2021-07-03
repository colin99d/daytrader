from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from .models import Topic, Message
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.token = self.scope['query_string'].decode("utf-8").split("=")[1]
        self.user = await self.get_user()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'topic': self.room_name,
                'user': self.user.username,
                'userId': self.user.id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        
        await self.save_message(message, self.room_name, self.user)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'topic': self.room_name,
            'user': self.user.username,
            'userId': self.user.id
        }))

    @database_sync_to_async
    def save_message(self, message, topic, user):
        topic = Topic.objects.get(name=topic)
        Message.objects.create(text=message,topic=topic,user=user)

    @database_sync_to_async
    def get_user(self):
        from django.contrib.auth.models import AnonymousUser
        try:
            return Token.objects.get(key=self.token).user
        except Token.DoesNotExist:
            return AnonymousUser()

