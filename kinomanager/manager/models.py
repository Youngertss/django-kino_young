from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class KinoUsers(AbstractUser):
    username = models.CharField(max_length=40, unique = True)
    money = models.IntegerField(default=0)
    is_support = models.BooleanField(default=False)
    # def save(self, *args, **kwargs):
    #     self.username = slugify(self.username)
    #     super().save(*args, **kwargs)


class Chat(models.Model):
    user_main = models.ForeignKey(KinoUsers, on_delete=models.CASCADE, related_name = "user_main")
    user_support = models.ForeignKey(KinoUsers, on_delete=models.CASCADE, related_name = "user_support")

class Message(models.Model):
    user = models.ForeignKey(KinoUsers, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)