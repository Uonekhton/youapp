from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from embed_video.fields import EmbedVideoField


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
		user.is_admin = True
		user.save(using=self._db)
		return user


class User(AbstractBaseUser):
	email = models.EmailField(
		verbose_name='email',
		max_length=255,
		unique=True,)
	balance = models.DecimalField(max_digits=2, decimal_places=0, default=0)
	first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True)
	last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True)
	is_active = models.BooleanField(verbose_name='Активный')
	is_admin = models.BooleanField(default=False, verbose_name='Администратор')

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


class Movie(models.Model):
	video = EmbedVideoField(verbose_name='Ссылка')
	price = models.DecimalField(max_digits=3, decimal_places=0, default=0, verbose_name='Цена')
	date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
	user = models.ForeignKey('User')
	thumbnail = models.CharField(verbose_name='thumbnail_url', max_length=255, blank=True)

	class Meta:
		ordering = ['-date']
		verbose_name = 'Видео'
		verbose_name_plural = 'Видео'
