from rest_framework import serializers
from .models import CustomUser,Chat,Message,Participant
from django.contrib.auth.hashers import make_password



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         validated_data['password'] = make_password(validated_data['password'])
#         return super().create(validated_data)




class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'content', 'sent_at', 'sender', 'sender_username']

    def get_sender_username(self, obj):
        return obj.sender.username if obj.sender else None

# class ChatSerializer(serializers.ModelSerializer):
#     messages = MessageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Chat
#         fields = ['chat_id', 'created_by', 'created_at', 'messages']

class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ['participant_id', 'user', 'username', 'joined_at']

    def get_username(self, obj):
        return obj.user.username if obj.user else None

class ChatListSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='created_by.username', read_only=True)
    latest_message = serializers.SerializerMethodField()
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['chat_id', 'created_by', 'created_at', 'latest_message','participants','creator_username']

    def get_latest_message(self, chat):
        latest_msg = chat.messages.order_by('-sent_at').first()
        if latest_msg:
            return MessageSerializer(latest_msg).data
        return None

class ChatDetailSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='created_by.username', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)


    class Meta:
        model = Chat
        fields = ['chat_id', 'created_by', 'created_at', 'messages','participants','creator_username']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)