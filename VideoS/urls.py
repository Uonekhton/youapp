from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.hmac.views import RegistrationView
from youapp.forms import MyCustomUserForm
from youapp.views import index, wall, add_movie, play_movie, LogoutView


urlpatterns = [
	url(r'^$', index,  name='index'),
	url(r'^admin/', admin.site.urls),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
	url(r'^auth/$', LogoutView.as_view(), name='auth'),
	url(r'^accounts/register/$', RegistrationView.as_view(form_class=MyCustomUserForm), name='register',),
	url(r'^accounts/', include('registration.backends.hmac.urls')),
	url(r'^add$', add_movie,  name='add'),
	url(r'^wall/(?P<user_id>\d+)/$', wall,  name='wall'),
	url(r'^movie/(?P<video_id>\d+)/$', play_movie,  name='movie')

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
