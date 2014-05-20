from ikarus_app.models import *
from django.http import *
import datetime
from models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.contrib import auth
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.contrib.auth import authenticate, login
import math

# Create your views here.
def home(request):
	html = "<html><h1 align='center'>Wellcome to </br> Ikarus Project App</h1></html>" 
	#return HttpResponse(html)
	return render( request, "base.html")


def d_image(request):
	a=Client.objects.get(nom="Dummy")
	ref = a.avatar
	html = "<html><p> %s. </p></html>" %ref
	return HttpResponse(html)


@login_required
def image(request):
	a=Client.objects.get(nom="admin")
	ref = a.avatar.read()
	return HttpResponse(ref, content_type="image/png")


@login_required
def user_profile(request):
	
	us = request.user.username #primer buscar el usuari de la sessio
	user=User.objects.get(username=us) # desar el objecte coresponent a USER
	client=Client.objects.get(username=user) # buscar el client que te relacio directa amb el USER desat

	#html = "<html><p> %s. </p></html>" %client.ref_client
	#return HttpResponse(html)
	return render( request, "profile.html", {"ref_client": client.ref_client, "Nom":client.nom ,"Cognoms":client.cognoms, "rating":client.rating, "location":client.location, "client":client}) #aixo ja funciona


#test to retrieve an image from the DB to the template 
def d_image_test(request):
	a=Client.objects.get(nom="Dummy")
	return render(request, "image_test.html", {"a":a})





@login_required
def user_inventory(request):
	us = request.user.username #primer buscar el usuari de la sessio
	user=User.objects.get(username=us) # desar el objecte coresponent a USER
	client=Client.objects.get(username=user) # buscar el client que te relacio directa amb el USER desat
	
	return render( request, "inventory.html", {"inventari": client.inventory}) #aixo ja funciona


@login_required
def user_quests(request):
	pass
	return render( request, "base.html")

@login_required
def user_friends(request):
	pass
	return render( request, "base.html")

@login_required
def user_map(request):
	pass
	return render( request, "base.html")


def contact(request):
	pass
	return render( request, "base.html")



def list_objects(request):
	pass
	return render( request, "base.html")


def quests(request):
	pass
	return render( request, "base.html")


def social(request):
	pass
	return render( request, "base.html")


def mobile_app(request):
	pass
	return render( request, "base.html")


def json_auth_web_service_out(request): # test data
	some_data_to_dump = {
	'nom': 'foo',
	'coord': '24 , 45 ',
	}
	data = simplejson.dumps(some_data_to_dump)
	return HttpResponse(data, mimetype='application/json')

@csrf_exempt
def json_auth_web_service_in(request):
	if request.method == 'POST':
		decoded_json = json.loads(request.body)
		#user = User.objects.filter(username=decoded_json['username'])
		
		print "+-------------# SERVER #-------------"
		print "| Request received! \n|Autentification started"
		print "| ...\n"

		username = decoded_json['username']
		password = decoded_json['password']
		user = authenticate(username=username, password=password)


		if user: 
			print "| Successful! User: "+ username+" has Loged In!"
			print "| ---> END OF COMUNICATION <---"
			print "+------------------------------------ \n\n\n"

			resultat= get_user_object_to_json(user)
			return HttpResponse(resultat, mimetype='application/json')
			
		else:
			print "| Access Denied! \n| Log In FAILED!\n| Please check Username and/or Password!"
			print "| ---> END OF COMUNICATION <---"
			print "+------------------------------------ \n\n\n"

			resultat="Server: Check Username and/or Password! "
			return HttpResponse(resultat, mimetype='application/json')
			
	else:
		print "+-------------# SERVER #-------------"
		print "| Request restricted to POST method"
		print "| Access Denied! \n | This attempt will be reported to the admins!"
		print "| ---> END OF COMUNICATION <---"
		print "+------------------------------------ \n\n\n"

	resultat="Server: Access Denied! /br Request restricted to POST method"
	return HttpResponse(resultat, mimetype='application/json')
	
			

#funcioa per pillar la lista del usuari i passarho cap al client movil via webservice
def get_user_object_to_json(user): 
	client=Client.objects.get(username=user) # buscar el client que te relacio directa amb el USER desat
	dic={"ref_client": client.ref_client, "Nom":client.nom ,"Cognoms":client.cognoms, "rating":client.rating, "location":client.location,"inventari": client.inventory}
	#print dic
	resultat=simplejson.dumps(dic)
	return resultat


@csrf_exempt
def json_movile_geo_objects(request):
	if request.method == 'POST':
		decoded_json = json.loads(request.body)
		#user = User.objects.filter(username=decoded_json['username'])
		longitude_user = decoded_json['longitude']
		latitude_user = decoded_json['latitude']

		#mostrar que hem rebut els datos7
		print "+-------------# SERVER #-------------"
		print "| Incoming request for Geo Location Items!"
		print "| . . . "
		print "| OK! Data has been received!"
		print "| Longitude: " +longitude_user
		print "| Latitude: " + latitude_user 
		print "| Searching for data . . . "

		resultat = torna_geo_items(longitude_user,latitude_user)

		print "| Data Found!"
		print "| Sending response to client!"
		print "| ---> END OF COMUNICATION <---"
		print "+------------------------------------ \n\n\n"


		return HttpResponse(resultat, mimetype='application/json')
			
	else:
		print "+-------------# SERVER #-------------"
		print "| Incoming request for Geo Location Items!"
		print "| ERROR! No data received!!"
		print "| ---> END OF COMUNICATION <---"
		print "+------------------------------------ \n\n\n"
		
		resultat="SERVER: ERROR! No data received!!"

	return HttpResponse(resultat, mimetype='application/json')



def torna_geo_items(longitude_user,latitude_user):
	lista_id_objectes=[10025, 10026, 10023, 10024, 10027]

	lista={"datos":[]}

	for i in lista_id_objectes:
		item = Objecte.objects.get(ref_objecte=i)
		if calcul_distancia_2_punts(longitude_user, latitude_user, item.longitude, item.latitude) <=500:
			dic = {"longitude":item.longitude, "latitude":item.latitude, "nom":item.nom}
			lista["datos"].append(dic)
		else:
			pass

	resultat=simplejson.dumps(lista)
	print resultat
	return resultat






def calcul_distancia_2_punts(x1,y1,x2,y2):
	suma = (float(x2)-float(x1))*(float(x2)-float(x1))+(float(y2)-float(y1))*(float(y2)-float(y1))
	d=math.sqrt(suma)
	resultat= d*100000
	return resultat

float()