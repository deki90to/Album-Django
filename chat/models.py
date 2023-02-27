from django.db import models
from datetime import datetime
from django.conf import settings


class Room(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return(f'{self.name} - room')


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

    def __str__(self): 
        return(f'{self.value} - message, {self.room} - room, {self.user} - user')

    class Meta:
        ordering = ['-date']


User = settings.AUTH_USER_MODEL

class ChatMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, null=True, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user}: {self.message}"
    
    class Meta:
        ordering = ['-created_on']