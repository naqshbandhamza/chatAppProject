# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat, Message, CustomUser
from .serializers import ChatListSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_id = text_data_json["senderId"]
        chat_id = text_data_json["chatId"]

        # Save message to DB
        try:
            sender = CustomUser.objects.get(user_id=sender_id)
            chat = Chat.objects.get(chat_id=chat_id)

            # Save message with sender and chat
            new_message = Message.objects.create(
                sender=sender,
                chat=chat,
                content=message,
                read_by=[sender.user_id]
            )

            # Serialize chat with latest message
            serializer = ChatListSerializer(chat)
            serialized_chat = serializer.data

            # Send to all users in the group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": serialized_chat,
                }
            )

        except CustomUser.DoesNotExist:
            self.send(text_data=json.dumps({"error": "Invalid sender."}))
        except Chat.DoesNotExist:
            self.send(text_data=json.dumps({"error": "Invalid chat."}))

    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event["message"]))



class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.username = self.scope["url_route"]["kwargs"]["username"]
        self.user_group_name = f"notifications_{self.username}"

        async_to_sync(self.channel_layer.group_add)(
            self.user_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.user_group_name, self.channel_name
        )

    def receive(self, text_data):
        # Not needed for this use case — this is a one-way notification
        pass

    def send_notification(self, event):
        self.send(text_data=json.dumps({
            "type": "notification",
            "data": event["data"],
        }))
