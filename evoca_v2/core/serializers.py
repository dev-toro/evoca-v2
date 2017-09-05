
from rest_framework import serializers as serial
from django.contrib.auth.models import User
from core.models import *

class DimensionSerializer(serial.ModelSerializer):
	class Meta:
		model = Dimension
		fields = ('id', 'uniqueID', 'name', 'slug' )

class ChannelSerializer(serial.ModelSerializer):
	dimensions = DimensionSerializer(many=True, read_only=True)
	class Meta:
		model = Channel
		fields = ('uniqueID', 'name', 'slug', 'about', 'dimensions', 'created_at', 'updated_at')
		read_only_fields = ('created_at', 'updated_at',)

class RecordSerializer(serial.ModelSerializer):

	class Meta:
		model = Record
		fields = ('uniqueID', 'author', 'channel', 'location', 'description', 'created_at', 'updated_at', )
		read_only_fields = ('created_at', 'updated_at',)
