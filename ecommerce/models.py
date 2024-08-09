from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from .validators import validate_no_special_characters

class User(AbstractUser):
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=15)
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={
            "unique": "A user is already registered with this nickname."
        }
    )
    address = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    country = CountryField(blank_label='(select country)')
    province = models.CharField(max_length=2)
    postalCode = models.CharField(max_length=6)
    history = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(verbose_name="Date Created", auto_now_add=True, null=True)

    def __str__(self):
        return self.email


class Item(models.Model):
    name = models.CharField(max_length=15)
    category = models.CharField(max_length=15)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=15)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    paymentId = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'Order {self.id} by {self.first_name} {self.last_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.item.name} (x{self.quantity})'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart for {self.user.email}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.item.name} (x{self.quantity})'

class Review(models.Model):
    rate = models.PositiveIntegerField()
    comment = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'Review by {self.user.email} for {self.item.name}'