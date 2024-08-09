from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView

from .models import Item

def index(request):
    return render(request, "ecommerce/index.html")

class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("index")

def item_list(request):
    items = Item.objects.all()
    context = {"items": items}
    return render(request, "ecommerce/item_list.html", context)

def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {"item": item}
    return render(request, "ecommerce/item_detail.html", context)

def user_profile(request):
    return render(request, "ecommerce/user_profile.html")