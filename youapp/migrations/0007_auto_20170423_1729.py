# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 12:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youapp', '0006_auto_20170423_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wall',
            name='user',
        ),
        migrations.AlterField(
            model_name='movie',
            name='wall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Wall',
        ),
    ]
