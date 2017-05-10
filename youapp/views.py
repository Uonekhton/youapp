import httplib2, requests, os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout, views
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from random import choice
from string import ascii_uppercase
from .forms import MovieForm, PayOutForm, Pay
from .models import Movie, User, Money
from constance import config
from decimal import *
from django.contrib import messages
from django.core.mail import send_mail


# Главна страница, колчество отображаемых видео задается в админке
def index(request):
	movie = Movie.objects.all()[:config.INDEX_MOVIE]
	return render(request, 'wall.html', {'movie': movie})


# Стена пользователя с видео
def wall(request, user_id):
	movie = Movie.objects.filter(author=user_id)
	return render(request, 'wall.html', {'movie': movie})


# Воспроизведение видео, проверяет является ли пользователь автором, или видео находится в списке купленных
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
			user.balance = user.balance+(movie.price*Decimal(config.COEFFICIENT))
			user.save()
			return render(request, 'movie.html', {'movie': movie})
		else:
			messages.warning(request, "Недостаточно средств")
		return redirect(request.META.get('HTTP_REFERER'))


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
	return {'thumb': '/static/img/%s.jpg' % name, 'title': title[0]}


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


# Удаление видео
@login_required
def del_movie(request, video_id):
	movie = Movie.objects.get(id=video_id)
	user = User.objects.get(id=request.user.id)
	if request.user == movie.author:
		try:
			path = '%s%s' % (settings.STATICFILES_DIRS[1], movie.thumbnail.replace('/static/', ''))
			os.remove(path)
		except FileNotFoundError:
			pass
		movie.delete()
		return redirect(request.META.get('HTTP_REFERER'))
	else:
		return redirect(request.META.get('HTTP_REFERER'))


class LogoutView(View):
	def get(self, request):
		logout(request)

		return HttpResponseRedirect("/")


def pay(request):
	if request.method == 'POST':
		form = Pay(request.POST)
	else:
		form = Pay()
	return render(request, "pay.html", {'form': form})


def pay_out(request):
	if request.method == 'POST':
		form = PayOutForm(request.POST)
		if form.is_valid():
			user = User.objects.get(id=request.user.id)
			money = form.cleaned_data['money']
			if user.balance - form.cleaned_data['balance'] >= 0:
				if form.cleaned_data['balance'] >= config.MIN_OUT:
					balance = user.balance
					user.balance = user.balance - form.cleaned_data['balance']
					user.save()
					form_valid = form.save(commit=False)
					form_valid.user = user
					form_valid.save()
					messages.success(request, "Заявка на вывод средств отправлена.")
					send_mail('%s - Вывод средств' % config.SITE_NAME,
							'Аккаунт %s \n'
							'Баланс %s \n'
							'Сумма: %s \n'
							'Способ вывода: %s \n'
							'Номер счета: %s \n' % (user.email, balance, form.cleaned_data['balance'], money.title, form.cleaned_data['score']),
							'from@example.com',
							[config.EMAIL_OUT], fail_silently=False)
				else:
					pass
			else:
				messages.warning(request, "На вашем балансе недостаточно средств.")
			return redirect(request.META.get('HTTP_REFERER'))
		else:
			pass
	else:
		form = PayOutForm()
	return render(request, "pay-out.html", {'form': form})


def paid(request):
	if request.method == 'POST':
		pass
	return render(request, 'pay.html')


def fail(request):
	if request.method == 'POST':
		pass
	return render(request, 'pay.html')