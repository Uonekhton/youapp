# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 12:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youapp', '0005_auto_20170423_1723'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'verbose_name': 'Видео', 'verbose_name_plural': 'Видео'},
        ),
        migrations.AddField(
            model_name='movie',
            name='wall',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='youapp.Wall'),
            preserve_default=False,
        ),
    ]
