from django.db import models
from apps.users_app.models import User


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    host = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="hosted_rooms")
    participants = models.ManyToManyField(
        User, related_name="participated_rooms")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="massages")
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="room_messages")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.body)[0:50]
