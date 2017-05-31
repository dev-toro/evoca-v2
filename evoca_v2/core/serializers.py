
from rest_framework import serializers as serial
from core.models import *

class DimensionSerializer(serial.ModelSerializer):
	class Meta:
		model = Dimension
		fields = ('id', 'uniqueID', 'name', 'slug' )

class ChannelSerializer(serial.ModelSerializer):
	dimensions = DimensionSerializer(many=True, read_only=True)
	class Meta:
		model = Channel
		fields = ('name', 'about', 'dimensions', 'created_at', 'updated_at')
		read_only_fields = ('created_at', 'updated_at',)

class OjovozRecordSerializer(serial.ModelSerializer):

	class Meta:
		model = OjovozRecord
		fields = ('uniqueID', 'author', 'channel', 'location', 'about', 'image', 'created_at', 'updated_at', )
		read_only_fields = ('created_at', 'updated_at',)
