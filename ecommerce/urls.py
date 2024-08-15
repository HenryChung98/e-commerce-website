from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.index, name='index'),
    # cart
    path("cart/", views.cart_list, name='cart-list'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase-quantity'),
    path('cart/remove/<int:item_id>/', views.decrease_quantity, name='decrease-quantity'),
    path('cart/delete/<int:item_id>/', views.remove_item, name='remove-item'),
    
    # items
    path("items/", views.item_list, name='item-list'),
    path("items/<int:item_id>/", views.item_detail, name='item-detail'),
    path("items/<int:item_id>/review", views.create_review, name='create-review'),
    
    # order
    path('order/', views.order_form, name='order-form'),
    path('order/payment/', views.process_payment, name='process_payment'),
    path('order/payment/success/', TemplateView.as_view(template_name="success.html"), name='payment_success'),
    path('order/payment/failed/', TemplateView.as_view(template_name="failed.html"), name='payment_failed'),
    
    # etc
    path("profile/<int:user_id>/", views.user_profile, name='user-profile'),
]
