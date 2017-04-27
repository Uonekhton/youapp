import httplib2, requests, json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout, views
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from random import choice
from string import ascii_uppercase
from .forms import MovieForm
from .models import Movie, User


def index(request):
	movie = Movie.objects.all()[:settings.INDEX_MOVIE]
	return render(request, 'wall.html', {'movie': movie})


def wall(request, user_id):
	movie = Movie.objects.filter(author=user_id)
	return render(request, 'wall.html', {'movie': movie})


@login_required
def play_movie(request, video_id):
	movie = Movie.objects.get(id=video_id)
	user = User.objects.get(id=request.user.id)
	if request.user == movie.author:
		return render(request, 'movie.html', {'movie': movie})
	elif user.purchased.filter(pk=movie.pk).exists() == True:
		return render(request, 'movie.html', {'movie': movie})
	else:
		if request.user.balance >= movie.price:
			user.balance = user.balance-movie.price
			user.purchased.add(movie)
			user.save()
			user = movie.author
			user.balance = user.balance+movie.price
			user.save()
			return render(request, 'movie.html', {'movie': movie})
		else:
			error = 'На вашем счете недостаточно средств.'
			return render(request, 'error.html', {'error': error})


# Функция определяет какую ссылку вставил пользователь, и загружает по ней превью
def thumb_down(url):
	if url.find('t=') != -1:
		name = url.split('=')[1].split('&t')
		name = name[0]
		url2 = 'http://img.youtube.com/vi/%s/mqdefault.jpg' % name
	elif url.find('=') != -1:
		name = url.split('=')[1]
		url2 = 'http://img.youtube.com/vi/%s/mqdefault.jpg' % name
	else:
		name = url.replace('https://youtu.be/', '')
		url2 = 'http://img.youtube.com/vi/%s/mqdefault.jpg' % name
	url = requests.get(
		'https://www.googleapis.com/youtube/v3/videos?'
		'part=snippet'
		'&fields=items(snippet(title))'
		'&id=%s&key=AIzaSyBlhjhmXF2M9ZhobNSSgWHloEn5TX2aceU' % name)
	title = url.text.split('"title": "')[1].split('"\n')
	name = ''.join(choice(ascii_uppercase) for i in range(5)) + name
	h = httplib2.Http('.cache')
	response, content = h.request(url2)
	out = open('%s/img/%s.jpg' % (settings.STATICFILES_DIRS[1], name), 'wb')
	out.write(content)
	out.close()
	return {'thumb' :'/static/img/%s.jpg' % name, 'title': title[0]}


# Добавление видео
@login_required
def add_movie(request):
	if request.method == 'POST':
		form = MovieForm(request.POST)
		if form.is_valid():
			user = User.objects.get(id=request.user.id)
			form_valid = form.save(commit=False)
			form_valid.author = user
			gg = thumb_down(form_valid.video)
			form_valid.thumbnail = gg['thumb']
			form_valid.title = gg['title']
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
