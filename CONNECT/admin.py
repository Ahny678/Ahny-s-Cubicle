from django.contrib import admin
from .models import Bword, Category, Room, Message

# Register your models here.
admin.site.register(Bword)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(Room)
