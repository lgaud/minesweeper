# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-22 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_cell_is_clear'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='is_flagged',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cell',
            name='is_marked',
            field=models.BooleanField(default=False),
        ),
    ]
