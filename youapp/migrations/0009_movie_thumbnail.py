# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youapp', '0008_auto_20170423_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='thumbnail',
            field=models.CharField(default=1, max_length=255, verbose_name='thumbnail_url'),
            preserve_default=False,
        ),
    ]