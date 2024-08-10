from django.contrib import admin
from .models import User, Item, Order, OrderItem, Cart, CartItem, Review
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Review)
UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname", )}), )