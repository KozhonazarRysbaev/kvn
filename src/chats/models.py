from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Room(models.Model):
    title = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Members(models.Model):
    room = models.ForeignKey(Room, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='members', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('room', 'user')


class Message(models.Model):
    from_user = models.ForeignKey(Members, related_name='senders', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




