from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
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
	url(r'^accounts/register/$', RegistrationView.as_view(form_class=MyCustomUserForm), name='register',),
	url(r'^accounts/', include('registration.backends.hmac.urls')),
	url('^change-password/', auth_views.password_change, {
		'template_name': 'change-password.html',
		'post_change_redirect': '/change-password-done/'}, name='change-password'),
	url('^change-password-done/', auth_views.password_change_done, {
		'template_name': 'change-password-done.html'}, name='password_change_done'),
	url('^password-reset/', auth_views.password_reset, {'template_name': 'password-reset.html'}, name='password-reset'),
	url(r'^add$', add_movie,  name='add'),
	url(r'^wall/(?P<user_id>\d+)/$', wall,  name='wall'),
	url(r'^movie/(?P<video_id>\d+)/$', play_movie,  name='movie')

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
