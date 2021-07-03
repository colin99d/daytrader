from .models import Message, Topic
from django.contrib import admin


# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    pass

class TopicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)
admin.site.register(Topic, TopicAdmin)
