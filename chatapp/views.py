from django.shortcuts import render
from django.http import HttpResponse
from .serializers import UserSerializer, ChatListSerializer, ChatDetailSerializer,MessageSerializer
from .models import CustomUser,Chat,Message,Participant
from rest_framework import viewsets

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .permissions import IsAdminUserOnly

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework.decorators import api_view, permission_classes

from .validators import is_valid_username, is_valid_email

from django.db.models import Q

from chatapp.utils.notifications import send_new_chat_notification



# Create your views here.
def home(request):
    return HttpResponse('response here')

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')

        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        # ensure none are missing/empty
        missing = [field for field in ('username', 'password', 'email')
                   if not request.data.get(field)]
        if missing:
            return Response(
                {'error': f"Missing field(s): {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate username
        valid, error = is_valid_username(username)
        if not valid:
            return Response({'error': error}, status=400)

        # Validate email
        valid, error = is_valid_email(email)
        if not valid:
            return Response({'error': error}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'email already exists'}, status=400)

        user = CustomUser.objects.create_user(username=username, password=password, email=email,firstname=firstname,lastname=lastname)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get the token and response from super
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        # Create your own response object so you can attach cookie
        res = Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })

        return res  

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUserOnly]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUserOnly()]
        return [IsAuthenticated()]
   
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.none()  # Required for router registration
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Get all chat IDs where the user is a participant
        participant_chat_ids = Participant.objects.filter(user=user).values_list('chat_id', flat=True)

        # Return chats where user is either the creator or a participant
        return Chat.objects.filter(
            Q(created_by=user) | Q(chat_id__in=participant_chat_ids)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return ChatListSerializer
        elif self.action == 'retrieve':
            return ChatDetailSerializer
        return ChatDetailSerializer  # fallback

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        chat_id = self.request.query_params.get('chat')
        if chat_id:
            queryset = queryset.filter(chat_id=chat_id)
        return queryset

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_chat(request):
    user = request.user
    target_username = request.data.get('target_username')
    message_content = request.data.get('message')

    # Validate input
    if not target_username or not message_content:
        return Response(
            {'error': 'target_username and message are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get the target user
    try:
        target_user = CustomUser.objects.get(username=target_username)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Target user does not exist.'}, status=404)

    # Create the chat
    chat = Chat.objects.create(created_by=user)

    # Add participants (both users)
    Participant.objects.create(chat=chat, user=target_user)

    # Create the initial message
    Message.objects.create(
        chat=chat,
        sender=user,
        content=message_content,
        read_by=[user.user_id]
    )

    serializer = ChatDetailSerializer(chat, context={'request': request})

    #  Send real-time notification to target user
    send_new_chat_notification(to_username=target_username, chat_data={
        'chat': serializer.data,
        'message': 'Chat created and message sent.'
    })

    return Response({
        'chat': serializer.data,
        'message': 'Chat created and message sent.'
    }, status=201)


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})