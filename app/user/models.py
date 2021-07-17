from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.dispatch import receiver
from trader.models import Algorithm
from django.urls import reverse
from django.db import models
import os


class User(AbstractUser):
    selected_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE, blank=True, null=True)
    daily_emails = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    url = instance.request.build_absolute_uri(reverse('user:change_password', kwargs={"token":reset_password_token.key}))
    send_mail("Password Reset for Daytrader",url,"cdelahun@iu.edu",[reset_password_token.user.email])