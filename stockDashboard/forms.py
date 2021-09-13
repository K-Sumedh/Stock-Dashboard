from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import default_date

class LoginForm(forms.Form):

    Email_SI = forms.CharField(label='Email-SI', required=False,max_length=50, widget= forms.TextInput
                                (attrs={'placeholder':'Username'})
                               )

    Password_SI = forms.CharField(max_length=32, required=False,widget=forms.PasswordInput
                                    (attrs={'placeholder':'Password'})
                                  )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'User Name'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']


class WatchListForm(forms.Form):
    ticker = forms.CharField(label='ticker', required=False,max_length=10, widget= forms.TextInput
                                (attrs={'placeholder':'Ticker'}))

    trade_Date = forms.DateTimeField(label='tradeDate', required=True, initial=default_date)
    trade_Date.widget.attrs.update({'placeholder' : 'Trade Date'})

    Quantity = forms.IntegerField(label="Quantity", required=True)
    Quantity.widget.attrs.update({'placeholder': 'Quantity'})

    Price = forms.IntegerField(label="Price", required=True)
    Price.widget.attrs.update({'placeholder':'Price'})

    #Comment = forms.CharField(max_length=50)

class Search(forms.Form):
    search = forms.CharField(label='search', required=False,max_length=10, widget= forms.TextInput
                                (attrs={'placeholder':'Search'}))




