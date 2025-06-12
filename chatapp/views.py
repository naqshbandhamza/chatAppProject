from django.shortcuts import render
from django.http import HttpResponse
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework import viewsets

# Create your views here.
def home(request):
    return HttpResponse('response here')

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer