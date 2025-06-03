# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True, db_column='IdUser')
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

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True, db_column='IdChat')
    created_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        # on_update=models.CASCADE, 
        db_column='creatorUsername'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat'

    def __str__(self):
        return f"Chat {self.chat_id}"

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, db_column='IdPosts')
    title = models.CharField(max_length=45, db_column='title')
    content = models.CharField(max_length=500)
    image = models.CharField(max_length=255, blank=True, null=True, db_column='img')
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        # on_update=models.CASCADE, 
        db_column='fromuser'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return f"Post {self.post_id}: {self.title}"

class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True, db_column='IdParticipants')
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        # on_update=models.CASCADE,  
        db_column='userId',
        null=True
    )
    chat = models.ForeignKey(
        Chat, 
        on_delete=models.CASCADE,
        # on_update=models.CASCADE,  
        db_column='fromchat'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participants'
        unique_together = ('user', 'chat')

    def __str__(self):
        if self.user != None:
            return f"{self.user.username} in Chat {self.chat_id}"
        else:
            return f"null in Chat {self.chat_id}"

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, db_column='IdDocuments')
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        # on_update=models.CASCADE,   
        db_column='frompost'
    )
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        # on_update=models.CASCADE,  
        db_column='comment_by'
    )
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, db_column='comment_at')

    class Meta:
        db_table = 'comments'

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post_id}"

class Like(models.Model):
    like_id = models.AutoField(primary_key=True, db_column='IdLikes')
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        # on_update=models.CASCADE,  
        db_column='frompost'
    )
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        # on_update=models.CASCADE,  
        db_column='liked_by'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='liked_at')

    class Meta:
        db_table = 'likes'
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Like by {self.user.username} on Post {self.post_id}"

class Message(models.Model):
    message_id = models.AutoField(primary_key=True, db_column='IdMessages')
    content = models.CharField(max_length=500)
    sender = models.ForeignKey(
        CustomUser, 
        # on_update=models.CASCADE,
        on_delete=models.SET_NULL, 
        db_column='fromuser',
        null=True
    )
    chat = models.ForeignKey(
        Chat, 
        # on_update=models.CASCADE,
        on_delete=models.CASCADE,  
        db_column='fromchat'
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['sent_at']

    def __str__(self):
        if self.sender != None:
            return f"Message in Chat {self.chat_id} by {self.sender.username}"
        else:
            return f"Message in Chat {self.chat_id} by null"

class Follows(models.Model):
    follow_id = models.AutoField(primary_key=True, db_column='IdFollow')
    follower = models.ForeignKey(
        CustomUser,
        related_name='following_set',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomUser,
        related_name='followers_set',
        on_delete=models.CASCADE
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follows

    def __str__(self):
        return f"{self.follower} follows {self.following}"


