from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
<<<<<<< HEAD

from .models import User

=======
from .models import User

# Register your models here.
>>>>>>> chatImprovements

admin.site.register(User, UserAdmin)