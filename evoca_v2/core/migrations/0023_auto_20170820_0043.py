# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-20 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20170820_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='channeltag',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='record',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
