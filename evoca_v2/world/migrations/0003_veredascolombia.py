# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-13 19:02
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0002_veredascol'),
    ]

    operations = [
        migrations.CreateModel(
            name='VeredasColombia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dptompio', models.CharField(max_length=5)),
                ('codigo_ver', models.CharField(max_length=11)),
                ('nom_dep', models.CharField(max_length=50)),
                ('nomb_mpio', models.CharField(max_length=50)),
                ('nombre_ver', models.CharField(max_length=50)),
                ('vigencia', models.CharField(max_length=4)),
                ('fuente', models.CharField(max_length=50)),
                ('descripcio', models.CharField(max_length=50)),
                ('seudonimos', models.CharField(max_length=250)),
                ('area_ha', models.FloatField()),
                ('cod_dpto', models.CharField(max_length=2)),
                ('shape_area', models.FloatField()),
                ('shape_len', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]