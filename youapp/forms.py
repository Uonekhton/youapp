from registration.forms import RegistrationForm
from .models import User


class MyCustomUserForm(RegistrationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')