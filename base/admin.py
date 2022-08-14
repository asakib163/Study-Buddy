from django.contrib import admin

from base.models import Message, Rooom, Topic, User

# Register your models here.
admin.site.register(Rooom)
admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Message)