from django.forms import ModelForm
from django import forms
from registration.forms import RegistrationForm
from .models import User, Movie, Statement
from constance import config


class MyCustomUserForm(RegistrationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ('video', 'price')
        widgets = {
            'video': forms.URLInput(attrs={'class': 'form-control', 'rows': '1', 'style': 'resize:none',
                                           'required': ''}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'rows': '1', 'style': 'resize:none',
                                              'required': ''}),
        }


class PayOutForm(ModelForm):
    class Meta:
        model = Statement
        fields = ('balance', 'score', 'money')
        widgets = {
            'balance': forms.NumberInput(attrs={'required': '', 'min': config.MIN_OUT, 'value': config.MIN_OUT}),
        }

class Pay(forms.Form):
    WMI_MERCHANT_ID = forms.NumberInput()
    WMI_PAYMENT_AMOUNT = forms.NumberInput()
    WMI_CURRENCY_ID = forms.NumberInput()
    WMI_SUCCESS_URL = forms.CharField(max_length=100)
    WMI_FAIL_URL = forms.CharField(max_length=100)
    WMI_CULTURE_ID = forms.CharField(max_length=10)
    
    class Meta:
        fields = ('WMI_PAYMENT_AMOUNT', )
        widgets = {
            'WMI_PAYMENT_AMOUNT': forms.NumberInput(attrs={'required': '', 'value': '100'}),
        }