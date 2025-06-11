from django.urls import path
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet

app_name = 'chatapp'


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('',views.home,name="home"),
    path('', include(router.urls)), 
]
