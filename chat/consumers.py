import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        self.message_queue = asyncio.Queue()

    async def disconnect(self, close_code):
        await self.message_queue.join()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "send_message",
                "message": message,
                "username": username,
            })
        await self.message_queue.put(None)

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

        await self.message_queue.get()
        self.message_queue.task_done()
