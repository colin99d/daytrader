from django.contrib.auth.models import AbstractUser
from django.db import models
from trader.models import Algorithm

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    selected_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE, blank=True, null=True)
    daily_emails = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)