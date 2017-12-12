
from rest_framework import serializers as serial
from models import *
from core.models import *

class RecordSerializer(serial.ModelSerializer):
	img_url = serial.CharField()
	audio_url = serial.CharField()
	hora = serial.CharField()
	fecha = serial.CharField()
	latitud = serial.DecimalField(max_digits=40, decimal_places=30)
	longitud = serial.DecimalField(max_digits=40, decimal_places=30)
	class Meta:
		model = Record
		fields = ('pk', 'img_url',	'audio_url', 'description',	'fecha', 'hora', 'latitud',	'longitud')

class imagenSerializer(serial.ModelSerializer):
    class Meta:
        model = Imagen
        fields = ('pk','img', 'channel')

class AudioSerializer(serial.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('pk', 'audio', 'channel')
