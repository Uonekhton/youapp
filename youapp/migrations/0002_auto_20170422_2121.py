# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_user',
            field=models.EmailField(max_length=255),
        ),
    ]
