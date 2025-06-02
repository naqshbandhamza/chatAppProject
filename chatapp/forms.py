from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username",'firstname', 'lastname', 'email', 'phone', 'status', 'dob')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username",'firstname', 'lastname', 'email', 'phone', 'status', 'dob')