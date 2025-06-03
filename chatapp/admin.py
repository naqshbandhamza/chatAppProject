from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import Chat, Post, Participant, Comment, Like, Message


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("user_id","username", "is_staff", "is_active",'firstname', 'lastname', 'email', 'phone', 'status', 'dob')
    list_filter = ("username", "is_staff", "is_active",'firstname', 'lastname', 'email', 'phone', 'status', 'dob')
    fieldsets = (
        (None, {"fields": ("username","firstname","lastname","email")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2", "is_staff","firstname","lastname","email",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'created_by', 'created_at')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'title', 'content', 'image', 'author', 'created_at')

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'user', 'chat', 'joined_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'post', 'author', 'text', 'created_at')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('like_id', 'post', 'user', 'created_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'content', 'sender', 'chat', 'sent_at')