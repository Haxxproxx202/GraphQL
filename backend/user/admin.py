from django.contrib import admin

from .models import User


@admin.register(User)
class CustomUser(admin.ModelAdmin):
    list_display = ['id', 'username']
