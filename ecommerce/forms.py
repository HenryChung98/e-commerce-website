from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import User, Item, Order, OrderItem, Cart, CartItem, Review

    
class SignupForm(forms.ModelForm):
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control country-select-widget'})
    )
    class Meta:
        model = User
        fields = ["firstName", "lastName", "nickname", "address", "city", "country", "province", "postalCode"]

    def signup(self, request, user):
        user.nickname = self.cleaned_data["nickname"]
        user.firstName = self.cleaned_data["firstName"]
        user.lastName = self.cleaned_data["lastName"]
        user.address = self.cleaned_data["address"]
        user.city = self.cleaned_data["city"]
        user.country = self.cleaned_data["country"]
        user.province = self.cleaned_data["province"]
        user.postalCode = self.cleaned_data["postalCode"]
        user.save()


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = '__all__'


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'firstName', 
            'lastName', 
            'email', 
            'address', 
            'city',
            'province',
            'postalCode', 
        ]
        

class PaymentForm(forms.Form):
    name_on_card = forms.CharField(max_length=100, label="Name on Card")
    card_number = forms.CharField(max_length=16, label="Card Number")
    expiry_month = forms.CharField(max_length=2, label="Expiry Month (MM)")
    expiry_year = forms.CharField(max_length=4, label="Expiry Year (YYYY)")
    cvc = forms.CharField(max_length=4, label="CVC")