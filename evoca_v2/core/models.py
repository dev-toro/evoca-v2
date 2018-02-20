# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.conf import settings
from django.db import models
from django.contrib.gis.db import models as modelsGIS
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# Import GIS data
import googlemaps

# Available Models

class TimeBot(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(blank=True, null=True)

	def updateCreationDate(self, date):
		self.created_at = date
		self.save()

	class Meta:
		abstract = True

# ----------- CHANNEL ------------->

class Dimension(models.Model):
	uniqueID = models.UUIDField(default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	slug = models.SlugField(blank=True, null=True)

	def save(self, *args, **kwargs):
	    self.slug = slugify(self.name)
	    super(Dimension, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Channel(TimeBot):
	uniqueID = models.UUIDField(default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	slug = models.SlugField(blank=True, null=True)
	isActive = models.BooleanField(default=True)
	about = models.TextField(max_length=255, blank=True)
	members = models.ManyToManyField(User, through='Membership', through_fields=('channel', 'user'), related_name='channel_members')
	dimensions = models.ManyToManyField(Dimension, related_name='channel_dimensions', blank=True)
	image = models.ImageField(upload_to='static/img/', blank=True, null=True)
	maxZoom = models.SmallIntegerField(default=18, blank=False)
	defaultZoom = models.SmallIntegerField(default=13, blank=False)
	mapCenterLocation = modelsGIS.PointField(max_length=40, blank=False)

	def save(self, *args, **kwargs):
	    self.slug = slugify(self.name)
	    super(Channel, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Membership(TimeBot):
    channel = models.ForeignKey(Channel)
    user = models.ForeignKey(User)
	

# ----------- RECORD ------------->

class Tag(TimeBot):
	uniqueID = models.UUIDField(default=uuid.uuid4, editable=False)
	related_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='related_channel')
	name = models.CharField(max_length=255)
	slug = models.SlugField(blank=True, null=True)
	isActive = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
	    self.slug = slugify(self.name)
	    super(Tag, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.slug

class Record(TimeBot):

	uniqueID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='record_author')
	isActive = models.BooleanField(default=True)
	channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='record_channel')
	location = modelsGIS.PointField(max_length=40, null=False)
	country = models.CharField(max_length=50, blank=True)
	region = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=50, blank=True)
	postal_code = models.CharField(max_length=50, blank=True)
	neighborhood = models.CharField(max_length=50, blank=True)
	address = models.CharField(max_length=50, blank=True)
	description = models.TextField(max_length=255, blank=True)
	tags = models.ManyToManyField(Tag, related_name='record_tags', blank=True)

	def save(self, *args, **kwargs):
		try:
			# Googlemaps data
			gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_ACCESS_TOKEN)
			data = gmaps.reverse_geocode((self.location.y, self.location.x))[0]['address_components']
			self.address = self.getWorldData(data, 'route') + " " + self.getWorldData(data, 'street_number')
			self.neighborhood = self.getWorldData(data, 'locality')
			self.city = self.getWorldData(data, 'administrative_area_level_2')
			self.region = self.getWorldData(data, 'administrative_area_level_1')
			self.country = self.getWorldData(data, 'country')
			self.postal_code = self.getWorldData(data, 'postal_code')
		except Exception as e:
			print(e)
			pass

		super(Record, self).save(*args, **kwargs)

	def getWorldData(self, data, type):
		result = ""
		for f in data:
			try:
				if(f['types'][0] == type):
					result =  f['long_name']
			except Exception as e:
				raise
		return result

	def transformToEPSG(self):
		ct = CoordTransform(SpatialReference(4326), SpatialReference(3857))
		print(self.location.transform(ct))
		return self.location.transform(ct)

	def getRawLocation(self):
		return str(self.location.x) + "," + str(self.location.y);

	def getLongPlace(self):
		return self.address + ", " + self.region + ", " + self.city + ", " + self.country

	def getTags(self):
		tags = []
		for tag in self.tags.all():
			queryset = Tag.objects.get(uniqueID=tag.uniqueID)
			tags.append(queryset)
		return tags

	def getAttachedImage(self):
		queryset = Attachment.objects.values('url').filter(attachment_type=0).filter(related_record__uniqueID=self.uniqueID).first()
		return queryset if queryset != None else {'url': "/static/img/image.png"}

	def getAttachedAudio(self):
		return Attachment.objects.values('url').filter(attachment_type=3).filter(related_record__uniqueID=self.uniqueID).first()

	def __unicode__(self):
		return unicode(self.uniqueID)


# ----------- USERS/PROFILE ------------->


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# ----------- MESSAGE ------------->


class Message(TimeBot):

	uniqueID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_author')
	isCheck = models.BooleanField(default=False)
	channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='message_channel')
	record = models.ForeignKey(Record, on_delete=models.CASCADE, null=False, related_name='message_record')
	body = models.TextField(max_length=250, blank=True)


# ----------- ATTACHMENTS ------------->

class Attachment(TimeBot):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attachment_author')
	url = models.CharField(max_length=200, null=False)
	hashName = models.UUIDField(default=uuid.uuid4, editable=False)
	isActive = models.BooleanField(default=True)
	related_record = models.ForeignKey(Record, on_delete=models.CASCADE, null=False, related_name='related_record')

	# FIle type types
	ATTACHMENT_TYPE_CHOICES = (
	(0, 'image'),
	(1, 'video'),
	(2, 'file'),
	(3, 'sound'),
	)
	attachment_type = models.PositiveSmallIntegerField(default=0, choices=ATTACHMENT_TYPE_CHOICES)

	def __unicode__(self):
		return self.url


class ChannelType(models.Model):
	pass
