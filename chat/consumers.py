import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # fetch previous mesage from database
        previous_messages = await self.get_previous_messages()
        # Send previous messages to the user
        for message in previous_messages:
            await self.send(text_data=json.dumps({"message": message.message}))
    
    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        room = await self.get_room_by_name(self.room_name)
        # creating message 
        new_message = await self.create_message(user=self.user, message=message, room=room)

        # Send message to room group
        # chat.message is a reference to chat_message method.
        # message is the body of the event.
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": new_message.message}
        )
    
    async def chat_message(self, event):
        print(event)
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
    
    
    # method to create a message register.
    @database_sync_to_async
    def create_message(self, user, room, message):
        return Message.objects.create(user=user,message=message,room=room)


    @database_sync_to_async
    def get_room_by_name(self, room_name):
        return Room.objects.get(name=room_name)

    
    @database_sync_to_async
    def get_previous_messages(self, limit=10):
        # retrieve the last  'limit' number of messages
        return Message.objects.filter(room__name=self.room_name).order_by('-created_at')[:limit][::-1]