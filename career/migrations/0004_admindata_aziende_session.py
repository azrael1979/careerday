# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-15 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0003_auto_20180812_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admindata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sessions', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Aziende',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settore', models.TextField()),
                ('dislocazione', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('settore', models.IntegerField()),
                ('number', models.IntegerField()),
            ],
        ),
    ]
