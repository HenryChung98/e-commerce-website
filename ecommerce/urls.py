from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("cart/", views.cart_list, name='cart-list'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add-to-cart'),
    path('order/', views.order_form, name='order-form'),
    path("items/", views.item_list, name='item-list'),
    path("items/<int:item_id>/", views.item_detail, name='item-detail'),
    path("items/<int:item_id>/review", views.create_review, name='create-review'),
    path("profile/<int:user_id>/", views.user_profile, name='user-profile'),
]
