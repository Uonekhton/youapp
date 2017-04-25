from django.forms import ModelForm
from django import forms
from registration.forms import RegistrationForm
from .models import User, Movie


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
