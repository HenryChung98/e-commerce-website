from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("items/", views.item_list, name='item-list'),
    path("items/<int:item_id>/", views.item_detail, name='item-detail'),
    path("profile/", views.user_profile, name='user-profile'),
]
