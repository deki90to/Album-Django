from django.db import models
from datetime import datetime



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