# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-21 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0020_auto_20180821_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='hash',
            field=models.CharField(max_length=128),
        ),
    ]
