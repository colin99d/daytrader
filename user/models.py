from django.contrib.auth.models import AbstractUser
from django.db import models
from trader.models import Algorithm

# Create your models here.
<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
=======
class User(AbstractUser):
    selected_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE, blank=True, null=True)
    daily_emails = models.BooleanField(default=False)
>>>>>>> chatImprovements
    class Meta:
        db_table = 'auth_user'