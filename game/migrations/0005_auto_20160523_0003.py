# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-23 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_game_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='num_moves',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.CharField(choices=[('N', 'New'), ('A', 'Active'), ('W', 'Win'), ('L', 'Loss')], default='N', max_length=1),
        ),
    ]
