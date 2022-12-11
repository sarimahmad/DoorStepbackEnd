import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from accounts.models import *




class MyConsumer(AsyncWebsocketConsumer):
    @sync_to_async()
    def create_message(self):
        message = Chat.objects.create(text=self.message, user_id=self.user, room_id=self.room   )
        message.save()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print("GroupName: ", self.room_group_name)
        print("room_name", self.room_name)
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'Connected from django Channels'}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        self.message = data['message']
        self.user = data["user"]
        self.room = data['room_id']

        # send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': "chat_message",
                "room_id": self.room,
                'message': self.message,
                'user': self.user,
            }
        )
        await self.create_message()


    async def chat_message(self, event):
        send_message = event['message']
        user_id = event['user']
        room = event['room_id']

        # send message to room group

        await self.send(text_data=json.dumps(
            {
                "room_id": room,
                'message': send_message,
                'user': user_id,


            }
        )
        )




    async def disconnect(self, *args, **kwargs):
        print("Disconnect")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
