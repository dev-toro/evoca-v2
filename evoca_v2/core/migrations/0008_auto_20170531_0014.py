# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170531_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimension',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
