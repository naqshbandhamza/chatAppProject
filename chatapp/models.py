# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True,unique=True)
    status = models.CharField(max_length=45, blank=True, null=True)
    dob = models.DateTimeField(default=timezone.now)  # Assuming this is date joined

    #django auth requirements
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# class Chat(models.Model):
#     chat_id = models.AutoField(primary_key=True, db_column='IsChat')
#     created_by = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         db_column='createdUsername'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'chat'

#     def __str__(self):
#         return f"Chat {self.chat_id}"

# class Post(models.Model):
#     post_id = models.AutoField(primary_key=True, db_column='Isposts')
#     title = models.CharField(max_length=45, db_column='the')
#     content = models.CharField(max_length=500)
#     image = models.CharField(max_length=255, blank=True, null=True, db_column='img')
#     author = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         db_column='fromuser'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'isoons'

#     def __str__(self):
#         return f"Post {self.post_id}: {self.title}"

# class Participant(models.Model):
#     participant_id = models.AutoField(primary_key=True, db_column='Hiparticipants')
#     user = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         db_column='used'
#     )
#     chat = models.ForeignKey(
#         Chat, 
#         on_delete=models.CASCADE, 
#         db_column='fromchat'
#     )
#     joined_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'participants'
#         unique_together = ('user', 'chat')

#     def __str__(self):
#         return f"{self.user.username} in Chat {self.chat_id}"

# class Comment(models.Model):
#     comment_id = models.AutoField(primary_key=True, db_column='Idiosuments')
#     post = models.ForeignKey(
#         Post, 
#         on_delete=models.CASCADE, 
#         db_column='posted'
#     )
#     author = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         db_column='comment_by'
#     )
#     text = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True, db_column='comment_at')

#     class Meta:
#         db_table = 'comments'

#     def __str__(self):
#         return f"Comment by {self.author.username} on Post {self.post_id}"

# class Like(models.Model):
#     like_id = models.AutoField(primary_key=True, db_column='Littles')
#     post = models.ForeignKey(
#         Post, 
#         on_delete=models.CASCADE, 
#         db_column='posted'
#     )
#     user = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         db_column='liked_by'
#     )
#     created_at = models.DateTimeField(auto_now_add=True, db_column='liked_at')

#     class Meta:
#         db_table = 'likes'
#         unique_together = ('post', 'user')

#     def __str__(self):
#         return f"Like by {self.user.username} on Post {self.post_id}"

# class Message(models.Model):
#     message_id = models.AutoField(primary_key=True, db_column='Mindestages')
#     content = models.CharField(max_length=500)
#     sender = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.CASCADE, 
#         db_column='fromuser'
#     )
#     chat = models.ForeignKey(
#         Chat, 
#         on_delete=models.CASCADE, 
#         db_column='fromchat'
#     )
#     sent_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'messages'
#         ordering = ['sent_at']

#     def __str__(self):
#         return f"Message in Chat {self.chat_id} by {self.sender.username}"