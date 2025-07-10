from django.urls import path
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet,ChatViewSet,MessageViewSet
from .views import LoginView,RegisterView

app_name = 'chatapp'

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'chat', ChatViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('',views.home,name="home"),
    path('', include(router.urls)), 
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-new-chat/',views.create_new_chat,name="create new chat")
]
