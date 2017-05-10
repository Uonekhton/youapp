from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from embed_video.fields import EmbedVideoField
from decimal import *
from constance import config

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('Вы должны ввести email')

		user = self.model(
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(
			email,
			password=password,
		)
		user.is_active = True
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


# Модель пользователя
class User(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='email',
		max_length=255,
		unique=True,)
	balance = models.DecimalField(max_digits=99, decimal_places=2, default=0)
	purchased = models.ManyToManyField('Movie', verbose_name='Купленные видео', blank=True)
	number = models.IntegerField(verbose_name='Номер заказа', blank=True, null=True)
	first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True)
	last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True)
	is_active = models.BooleanField(verbose_name='Активный', default=False)
	is_admin = models.BooleanField(default=False, verbose_name='Администратор')
	is_superuser = models.BooleanField(default=False, verbose_name='Супер Администратор')

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	def email_user(self, *args):
		send_mail(
			'{}'.format(args[0]),
			'{}'.format(args[1]),
			'{}'.format(args[2]),
			[self.email],
		)

	def get_full_name(self):
		return '%s %s' % (self.last_name, self.first_name)

	def get_short_name(self):
		return self.email

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'


# Модель видео
class Movie(models.Model):
	title = models.CharField(verbose_name='Название', max_length=100)
	video = EmbedVideoField(verbose_name='Ссылка')
	price = models.DecimalField(max_digits=99, decimal_places=2, default=0, verbose_name='Цена')
	date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
	author = models.ForeignKey('User', verbose_name='Автор')
	thumbnail = models.CharField(verbose_name='thumbnail_url', max_length=255, blank=True)
	
	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-date']
		verbose_name = 'Видео'
		verbose_name_plural = 'Видео'


class Statement(models.Model):
	balance = models.DecimalField(max_digits=99, decimal_places=2,
								verbose_name='Сумма списания',
								help_text='Минимальная сумма вывода: %s' % config.MIN_OUT)
	score = models.CharField(verbose_name='Счет зачисления', max_length=45)
	date = models.DateTimeField(auto_now_add=True, verbose_name='Дата', blank=True)
	user = models.ForeignKey('User', verbose_name='Пользователь')
	money = models.ForeignKey('Money', verbose_name='Способ вывода')
	def __str__(self):
		return self.score
	
	class Meta:
		ordering = ['-date']
		verbose_name = 'Заявка на вывод'
		verbose_name_plural = 'Заявки на вывод'


class Money(models.Model):
	title = models.CharField(max_length=100)
	
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name = 'Способ вывода'
		verbose_name_plural = 'Способы вывода'