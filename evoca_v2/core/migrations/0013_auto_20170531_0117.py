# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170531_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='dimensions',
            field=models.ManyToManyField(blank=True, related_name='channel_dimensions', to='core.Dimension'),
        ),
    ]
