from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
