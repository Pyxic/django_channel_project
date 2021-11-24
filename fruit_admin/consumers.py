from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json

from fruit_admin.models import ChatMessage


class ProductCountConsumer(WebsocketConsumer):
    def connect(self):
        self.product_count_group_name = 'products_count'
        print("channel")
        async_to_sync(self.channel_layer.group_add)(
            self.product_count_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.discard)(
            self.product_count_group_name,
            self.channel_name
        )

    def update_count(self, event):
        print(event)
        self.send(text_data=json.dumps({"product": event['product'], "count": event['count'],
                                        "cash": event['cash']}))


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.chat_group_name = 'chat'
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.discard)(
            self.chat_group_name,
            self.channel_name
        )

# Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        new_message = self.create_chat_message(message)
        data = {
            'user': new_message.user.username,
            'text': new_message.text
        }
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': data
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def create_chat_message(self, text):
        new_message = ChatMessage.objects.create(user=self.scope['user'], text=text)
        return new_message


class JokesConsumer(WebsocketConsumer):
    def connect(self):
        # Подключает канал с именем `self.channel_name`
        # к группе `jokes`
        async_to_sync(self.channel_layer.group_add)(
            "jokes", self.channel_name
        )
        # Принимает соединение
        self.accept()

    def disconnect(self, close_code):
        # Отключает канал с именем `self.channel_name`
        # от группы `jokes`
        async_to_sync(self.channel_layer.group_discard)(
            "jokes", self.channel_name
        )

    # Метод `jokes_joke` - обработчик события `jokes.joke`
    def jokes_joke(self, event):
        # Отправляет сообщение по вебсокету
        self.send(text_data=json.dumps({"text": event['text'], "user": event['user']}))
