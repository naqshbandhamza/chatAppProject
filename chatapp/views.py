from django.shortcuts import render
from django.http import HttpResponse
from .serializers import UserSerializer, ChatSerializer
from .models import CustomUser,Chat
from rest_framework import viewsets

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .permissions import IsAdminUserOnly

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from .validators import is_valid_username, is_valid_email

# Create your views here.
def home(request):
    return HttpResponse('response here')

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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

        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUserOnly]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUserOnly()]
        return [IsAuthenticated()]

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [IsAdminUserOnly()]
    #     return [IsAuthenticated()]
