# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-21 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0021_auto_20180821_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='session',
            field=models.CharField(default='', max_length=128),
        ),
    ]
