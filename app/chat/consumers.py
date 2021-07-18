from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from .serializers import TopicSerializer
from .models import Topic, Message
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.token = self.scope['query_string'].decode("utf-8").split("=")[1]
        self.user = await self.get_user()
        self.topic = await self.get_topic()

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

        await self.save_message(message, self.room_name, self.user)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'topic': TopicSerializer(self.topic).data,
                'user': self.user.username,
                'user_id': self.user.id,
                'created_at': str(self.message.created_at)
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        
        

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'topic': TopicSerializer(self.topic).data,
            'user': self.user.username,
            'user_id': self.user.id,
            'created_at': str(self.message.created_at)
        }))

    @database_sync_to_async
    def save_message(self, message, topic, user):
        topic = Topic.objects.get(name=topic)
        self.message = Message.objects.create(text=message,topic=topic,user=user)

    @database_sync_to_async
    def get_user(self):
        from django.contrib.auth.models import AnonymousUser
        try:
            return Token.objects.get(key=self.token).user
        except Token.DoesNotExist:
            return AnonymousUser()

    @database_sync_to_async
    def get_topic(self):
        return Topic.objects.get(name=self.room_name)

