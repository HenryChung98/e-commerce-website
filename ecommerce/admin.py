from django.contrib import admin
from .models import User, Item
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Item)
UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname", )}), )