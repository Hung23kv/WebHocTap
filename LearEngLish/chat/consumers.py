from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Doithoai, Dtnguoidung, Nguoidung
from datetime import date
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

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

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            translated_message = text_data_json['translated_message']  # Tin nhắn đã dịch
            user_id = text_data_json['user_id']
            username = text_data_json['username']

            # Gửi tin nhắn đến room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'translated_message': translated_message,  # Gửi tin nhắn đã dịch
                    'user_id': user_id,
                    'username': username
                }
            )
        except Exception as e:
            print(f"Error in receive: {str(e)}")

    async def chat_message(self, event):
        try:
            message = event['message']
            translated_message = event['translated_message']  # Lấy tin nhắn đã dịch
            user_id = event['user_id']
            username = event['username']

            # Gửi tin nhắn đến WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'translated_message': translated_message,  # Gửi tin nhắn đã dịch
                'user_id': user_id,
                'username': username
            }))
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")

    @sync_to_async
    def save_message(self, user_id, message):
        user = Nguoidung.objects.get(id=user_id)
        chat_room = Doithoai.objects.get(id=self.room_id)
        Dtnguoidung.objects.create(
            nguoigui=user,
            tinnhan=message,
            ngay=date.today(),
            id_doithoai=chat_room
        )
