# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-25 22:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid
from django.contrib.auth.models import User
from core.models import Profile

def createProfiles():
    queryset = User.objects.all()
    for user in queryset:
        Profile.objects.create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0029_record_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('uniqueID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isCheck', models.BooleanField(default=False)),
                ('body', models.TextField(blank=True, max_length=250)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_author', to=settings.AUTH_USER_MODEL)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_channel', to='core.Channel')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_record', to='core.Record')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        createProfiles()
    ]
