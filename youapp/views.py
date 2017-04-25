import httplib2
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from random import choice
from string import ascii_uppercase
from .forms import MovieForm
from .models import Movie, User


def wall(request, user_id):
	movie = Movie.objects.filter(user=user_id)
	return render(request, 'wall.html', {'movie': movie})


# Воспроизведение видео
def play_movie(request, video_id):
	movie = Movie.objects.get(id=video_id)
	return render(request, 'movie.html', {'movie': movie})


# Функция определяет какую ссылку вставил пользователь, и загружает по ней превью
def thumb_down(url):
	if url.find('=') != -1:
		url2 = 'http://img.youtube.com/vi/%s/0.jpg' % url.split('=')[1]
		name = ''.join(choice(ascii_uppercase) for i in range(5))+url.split('=')[1]
	else:
		url2 = 'http://img.youtube.com/vi/%s/0.jpg' % url.replace('https://youtu.be/', '')
		name = ''.join(choice(ascii_uppercase) for i in range(5))+url.replace('https://youtu.be/', '')
	h = httplib2.Http('.cache')
	response, content = h.request(url2)
	out = open('%s/img/%s.jpg' % (settings.STATICFILES_DIRS[1], name), 'wb')
	out.write(content)
	out.close()
	return '/static/img/%s.jpg' % name


# Добавление видео
@login_required
def add_movie(request):
	if request.method == 'POST':
		form = MovieForm(request.POST)
		if form.is_valid():
			user = User.objects.get(id=request.user.id)
			form_valid = form.save(commit=False)
			form_valid.user = user
			form_valid.thumbnail = thumb_down(form_valid.video)
			form_valid.save()
			return redirect('/wall/%s' % user.id)
		else:
			pass
		return
	else:
		form = MovieForm()
	return render(request, "add_movie.html", {'form': form})


class LogoutView(View):
	def get(self, request):
		logout(request)

		return HttpResponseRedirect("/")
