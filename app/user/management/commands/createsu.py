from django.core.management.base import BaseCommand
from user.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin",os.environ.get("ADMIN_EMAIL"),os.environ.get("ADMIN_PASSWORD"))