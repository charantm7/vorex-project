import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatBox, Room
from django.contrib.auth.models import User

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'group_chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']

        user = await self.get_user(user_id)
        room = await self.get_room(self.room_name)

        # Save message to DB
        chat_message = await self.create_message(user, room, message)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat_message.content,
                'user': user.username,
                'created_at': str(chat_message.created_at)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'created_at': event['created_at']
        }))

    @staticmethod
    async def get_user(user_id):
        return await User.objects.aget(id=user_id)

    @staticmethod
    async def get_room(room_name):
        return await Room.objects.aget(name=room_name)

    @staticmethod
    async def create_message(user, room, message):
        return await ChatBox.objects.acreate(user=user, room=room, content=message)
