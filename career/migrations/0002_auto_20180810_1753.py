# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-10 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('rank', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='question',
            old_name='rank',
            new_name='page',
        ),
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=1500),
        ),
        migrations.AddField(
            model_name='skill',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career.Question'),
        ),
    ]
