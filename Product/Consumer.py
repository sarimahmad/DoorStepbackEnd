import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MyConsumer(AsyncWebsocketConsumer):
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
        print(data)
        message = data['message']
        _id = data['_id']
        user = data["user"]

        # send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': "chat_message",
                'message': message,
                'user': user,
                '_id': _id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        _id = event['_id']
        user = event['user']

        # send message to room group
        await self.send(text_data=json.dumps(
            {
                'message': message,
                'user': user,
                '_id': _id,

            }
        )
        )

    async def disconnect(self, *args, **kwargs):
        print("Disconnect")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
