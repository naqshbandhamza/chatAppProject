# chat/utils/notifications.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_new_chat_notification(to_username, chat_data):
    channel_layer = get_channel_layer()
    group_name = f"notifications_{to_username}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "data": {
                "message": "You have a new chat!",
                "chat": chat_data,
            },
        }
    )
