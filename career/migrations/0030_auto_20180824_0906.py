# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-24 07:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0029_auto_20180824_0900'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='aperta',
            new_name='chiusa',
        ),
    ]
