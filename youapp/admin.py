from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from embed_video.admin import AdminVideoMixin
from .models import Movie, Statement, Money

from .models import User
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('email',)

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name')
    list_filter = ('is_admin', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'balance', 'purchased')}),
        ('Доступ', {'fields': ('is_admin', 'is_active')})
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
                ('Персональная информация', {'fields': ('first_name', 'last_name', 'purchased')}),
                ('Доступ', {'fields': ('is_admin', 'is_active')})
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'date')
    list_filter = ('price', 'author', 'date')
    ordering = ('date',)


class StatementAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date')
    list_filter = ('user', 'score', 'date')
    ordering = ('date',)


admin.site.register(Movie, MyModelAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Money)
admin.site.register(Statement, StatementAdmin)