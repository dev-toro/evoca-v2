# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 00:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20170531_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='dimensions',
            field=models.ManyToManyField(related_name='channel_dimensions', to='core.Dimension'),
        ),
    ]
