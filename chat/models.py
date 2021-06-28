from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text