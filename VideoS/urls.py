from django.conf.urls import include, url
from django.contrib import admin
from registration.backends.hmac.views import RegistrationView
from youapp.forms import MyCustomUserForm

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=MyCustomUserForm), name='registration_register',),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

]
