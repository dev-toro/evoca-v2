# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-01 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_remove_record_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='record_tags', to='core.Tag'),
        ),
    ]
