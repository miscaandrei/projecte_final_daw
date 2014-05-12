from django.db import models
from django.contrib.auth.models import User # fem un import de la llibreria de usuaris de sistema de django, aixis que quan creem un usuari de sistema passa a ser automaticament un client
from django.db.models.signals import post_save # despres de crear el usuari de sistema quens crei el client tambe
from django.contrib.gis.db import models
from django.contrib import admin
from models_admin import *
# Create your models here.


class Client(models.Model):
	"""docstring for Client"""
	username=models.OneToOneField(User)
	ref_client=models.IntegerField()
	nom=models.CharField(max_length=250)
	cognoms=models.CharField(max_length=250)
	email=models.EmailField()
	rating=models.SmallIntegerField()
	friends=models.CharField(max_length=250) #dins d'aquesta variable desarem una llista json que contindra una llista de tots els items que tenim
	location=models.CharField(max_length=250) #desa dins l'ubicacio en forma deJSOn amb Lon Lat
	avatar=models.ImageField(upload_to = 'pic_folder/')
	description=models.CharField(max_length=250)
	completed_quests=models.CharField(max_length=250) # llista JSON
	inventory=models.CharField(max_length=250) # llista JSON
	#def image_(self):
		#return '<a href="/media/{0}"><img src="/media/{0}"></a>'.format(	)
	#image_.allow_tags = True


class Objecte(models.Model):
	"""docstring for Objecte"""

	ref_objecte=models.IntegerField()
	nom=models.CharField(max_length=250)
	description=models.CharField(max_length=250)
	arxiu=models.CharField(max_length=250) # objecte desat en format JSON
	dimensions=models.CharField(max_length=250) #lista JSON amb x,y,z
	posicio=models.CharField(max_length=250) #desa dins l'ubicacio en forma deJSOn amb Lon Lat


class Quests(models.Model):
	"""docstring for Quests"""
	nom=models.CharField(max_length=250)
	description=models.CharField(max_length=250)
	reward=models.CharField(max_length=250)
	min_rating=models.IntegerField()






admin.site.register(Client, Client_admin)
admin.site.register(Objecte, Objecte_admin)
admin.site.register(Quests, Quests_admin)