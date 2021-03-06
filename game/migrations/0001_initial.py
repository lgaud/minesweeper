# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-21 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_loc', models.IntegerField(default=0)),
                ('y_loc', models.IntegerField(default=0)),
                ('has_mine', models.BooleanField(default=False)),
                ('num_adjacent_mines', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_cells', models.IntegerField(default=9)),
                ('y_cells', models.IntegerField(default=9)),
                ('num_mines', models.IntegerField(default=10)),
            ],
        ),
        migrations.AddField(
            model_name='cell',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game'),
        ),
    ]
