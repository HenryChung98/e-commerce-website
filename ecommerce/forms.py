from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import User

    
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

