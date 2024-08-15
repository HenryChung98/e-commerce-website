from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings

from .models import User, Item, Order, OrderItem, Cart, CartItem, Review
from .forms import ReviewForm, OrderForm, PaymentForm

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
    reviews = Review.objects.filter(item=item)

    context = {
        "item": item,
        "reviews": reviews,
        "cart": cart,
        "cart_items": CartItem.objects.filter(cart=cart),
    }

    return render(request, "ecommerce/item_detail.html", context)


@login_required
def increase_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart-list')

@login_required
def decrease_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart-list')

@login_required
def remove_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
    cart_item.delete()
    return redirect('cart-list')


# profile
@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(user=user)
    orders = Order.objects.filter(user=user)
    orderItems = OrderItem.objects.filter(order__in=orders)

    context = {
        'user': user,
        'reviews': reviews,
        "orders": orders,
        "orderItems": orderItems
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
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            cart_items = request.session.get('cart_items')

            if not cart_items:
                return redirect('cart-list')

            # 세션에 Order 및 OrderItems 데이터 저장
            order_data = {
                'user_id': request.user.id,
                'form_data': order_form.cleaned_data,  # OrderForm에서 받은 데이터를 저장
                'items': cart_items  # 장바구니 아이템을 세션에 저장
            }
            request.session['order_data'] = order_data

            return redirect('process_payment')
    else:
        order_form = OrderForm()

    cart_items = request.session.get('cart_items', [])
    total_amount = sum(
        float(item['quantity']) * float(item['price'])
        for item in cart_items
    )

    context = {
        'form': order_form,
        'cart_items': cart_items,
        'total': total_amount
    }

    return render(request, "forms/order_form.html", context)


stripe.api_key = settings.STRIPE_SECRET_KEY

def process_payment(request):
    # 세션에서 Order 데이터 가져오기
    order_data = request.session.get('order_data')
    if not order_data:
        return redirect('cart-list')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            token = request.POST.get('stripeToken')
            try:
                # 결제 처리
                total_amount = sum(
                    float(item['quantity']) * float(item['price'])
                    for item in order_data['items']
                )
                charge = stripe.Charge.create(
                    amount=int(total_amount * 100),  # 센트 단위로 금액 설정
                    currency='usd',
                    description=f"Order by {request.user.email}",
                    source=token,
                )

                # Order 및 OrderItems 데이터베이스에 저장
                order = Order.objects.create(
                    user_id=order_data['user_id'],
                    is_paid=True,
                    paymentId=charge['id'],
                    **order_data['form_data']  # OrderForm에서 받은 데이터 언패킹하여 저장
                )

                for item in order_data['items']:
                    OrderItem.objects.create(
                        order=order,
                        item_id=item['item_id'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

                # 장바구니 비우기 및 세션 데이터 삭제
                user_cart = Cart.objects.get(user=request.user)
                user_cart.cart_items.all().delete()
                del request.session['order_data']

                return redirect('payment_success')

            except stripe.error.CardError:
                order.is_paid = False
                order.save()
                return redirect('payment_failed')

    else:
        form = PaymentForm()

    return render(request, 'forms/process_payment.html', {'form': form})
