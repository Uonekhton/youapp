# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 18:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('youapp', '0002_auto_20170422_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_user',
        ),
    ]