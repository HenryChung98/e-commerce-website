from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from django.contrib.auth.decorators import login_required

from .models import User, Item, Order, OrderItem, Cart, CartItem, Review
from .forms import ReviewForm, OrderForm

def index(request):
    return render(request, "ecommerce/index.html")

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("index")


# items 
def item_list(request):
    items = Item.objects.all()
    context = {"items": items}
    return render(request, "ecommerce/item_list.html", context)

def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    reviews = Review.objects.filter(item=item)
    context = {"item": item,
                "reviews": reviews
            }
    return render(request, "ecommerce/item_detail.html", context)


# cart
def cart_list(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_amount = sum(item.quantity * item.price for item in cart_items)

    cart_items_data = [
        {
            'item_id': item.item.id,
            'item_name': item.item.name,
            'quantity': item.quantity,
            'price': str(item.price) 
        }
        for item in cart_items
    ]
    request.session['cart_items'] = cart_items_data
    context = {
        "cart": cart,
        "cart_items": cart_items,
        "total": total_amount
    }
    return render(request, "ecommerce/cart.html", context)


@login_required
def add_to_cart(request, item_id):
    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get the item to be added to the cart
    item = get_object_or_404(Item, id=item_id)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        item=item,
        cart=cart,
        defaults={'quantity': 1, 'price': item.price}
    )
    
    if not created:
        # If the item already exists in the cart, update the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('item-list')  # Redirect to wherever you want after adding to the cart


@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(user=user)
    orders = Order.objects.filter(user=user)
    context = {
        'user': user,
        'reviews': reviews,
        "orders": orders
    }
    return render(request, "ecommerce/user_profile.html", context)



# forms
@login_required
def create_review(request, item_id):
    item = Item.objects.get(id=item_id)
    review_form = ReviewForm()

    if request.method == 'POST':
        rate = request.POST.get('rate') 
        comment = request.POST.get('comment')  

        # Create and save the Review instance
        review = Review(
            item=item,
            user=request.user, 
            rate=rate,
            comment=comment
        )
        review.save()
        return redirect('item-detail', item_id=item_id)

    context = {
        'item': item,
        'form': review_form
    }
    return render(request, "forms/review_form.html", context)

@login_required
def order_form(request):
    order_form = OrderForm()
    cart_items = request.session.get('cart_items')
    total_amount = sum(
        float(item['quantity']) * float(item['price'])
        for item in cart_items
    )

    if cart_items is None:
        return redirect('cart-list')

    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        province = request.POST.get('province')
        postalCode = request.POST.get('postalCode')

        order = Order(
            user=request.user, 
            firstName=firstName,
            lastName=lastName,
            email=email,
            address=address,
            city=city,
            country=country,
            province=province,
            postalCode=postalCode,
# is_paid, paymentId
        )
        order.save()
        return redirect('item-list')

    context = {
        'form': order_form,
        'cart_items': cart_items,
        'total' :total_amount
    }

    return render(request, "forms/order_form.html", context)