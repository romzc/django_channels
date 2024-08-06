from django.contrib import admin
from .models import Room, User, Message

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)