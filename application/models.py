from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from application.storage import OverwriteStorage
from django.dispatch import receiver
from django.db.models.signals import post_delete
from decimal import Decimal




class vrijeme_promet(models.Model):
	vrijeme = models.DateTimeField(db_index=True)
	promet  = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, db_index=True)
	class Meta:
		verbose_name = "Promet"
		verbose_name_plural = "Prometmin"
	def __unicode__(self):
		return '%s %s' % (self.vrijeme, self.promet)


class Requests_vrijeme(models.Model):
	vrijeme  = models.DateTimeField(db_index=True)
	requests = models.BigIntegerField(db_index=True)
	class Meta:
		verbose_name = "Request"
		verbose_name_plural = "Requestmin"
	def __unicode__(self):
		return '%s %s' % (self.vrijeme, self.requests)


class Status(models.Model):
	status = models.BigIntegerField(db_index=True)
	brojponavljanja = models.BigIntegerField(db_index=True)
	

class Najaktivniji(models.Model):
	ip = models.CharField(max_length=225, db_index= True)
	brojponavljanja = models.BigIntegerField(db_index=True)
	class Meta:
		verbose_name = "clineti"
		verbose_name_plural = "ipclienti"
	def __unicode__(self):
		return '%s %s' % (self.ip, self.brojponavljanja)


class Contents(models.Model):
	content = models.CharField(max_length=225, db_index= True)
	brojponavljanja = models.BigIntegerField(db_index=True)
	class Meta:
		verbose_name = "content"
		verbose_name_plural = "contentss"
	def __unicode__(self):
		return '%s %s' % (self.content, self.brojponavljanja)

class Document(models.Model):

	docfile = models.FileField(blank=True, null=True, storage=OverwriteStorage(),upload_to='upload')
	def delete(self, *args, **kwargs):
		self.docfile.delete()
		super(Document, self).delete(*args, **kwargs)

 
class nginxLog(models.Model):

	ip = models.CharField(max_length=225)
	vrijeme = models.DateTimeField()
	request = models.CharField(max_length=225)
	status = models.BigIntegerField()
	bandwidth = models.BigIntegerField()
	user_agent = models.CharField(max_length=225)
	referrer = models.CharField(max_length=225)

	
class status_per_hour206(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)


class status_per_hour200(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)


class status_per_hour404(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)


class status_per_hour301(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)


class status_per_hour302(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)


class status_per_hour403(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)

class status_per_hour405(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)

class status_per_hour406(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)

class status_per_hour500(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)	


class status_per_hour504(models.Model):
	time = models.DateTimeField(null=True)
	y = models.IntegerField(db_index=True)	

class ipcontent(models.Model):

	ip = models.CharField(max_length=225)	
	content = models.CharField(max_length=225)
	counts = models.IntegerField()


class overall(models.Model):

	promet = models.CharField(max_length=225,null=True)
	code200 = models.IntegerField(null=True)
	code404 = models.IntegerField(null=True)
	ip = models.IntegerField(null=True)
	content = models.IntegerField(null=True)
	fajl = models.CharField(max_length=225, null=True)
	code = models.IntegerField(null=True)
	total = models.IntegerField(null=True)
	metod = models.IntegerField(null=True)
	status400 = models.IntegerField(null=True)
	status403 = models.IntegerField(null=True)
	scripttime = models.CharField(max_length=225,null=True)

