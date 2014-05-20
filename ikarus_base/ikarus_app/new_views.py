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


def json_auth_web_service_out(request):
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
		username = decoded_json['username']
		password = decoded_json['password']
		user = authenticate(username=username, password=password)
		if user: 
			print "ok. loged in"
			resultat= get_user_object_to_json(user)
			return HttpResponse(resultat, mimetype='application/json')
			
		else:
			print "invalid"
			
	else:
		print "login error"

	resultat="Log In ERROR"
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
		longitude = decoded_json['longitude']
		latitude = decoded_json['latitude']
		print "dades rebudes "
		print longitude
		print latitude
		resultat = "OK! dades rebudes"
		objecte_1=Objecte.objects.get(ref_objecte=10025)
		dic_1 = {"longitude":objecte_1.longitude, "latitude":objecte_1.latitude, "nom":objecte_1.nom}
		lista=[]
		objecte_2=Objecte.objects.get(ref_objecte=10026)	
		dic_2 = {"longitude":objecte_2.longitude, "latitude":objecte_2.latitude, "nom":objecte_2.nom}
		lista={"datos":[dic_1, dic_2]}
		resultat=simplejson.dumps(lista)
		print resultat
		print "enviant resposta "
		return HttpResponse(resultat, mimetype='application/json')
			
	else:
		print "UPS! res rebut  error"
		resultat="ERROR, no funciona del servidor "
	return HttpResponse(resultat, mimetype='application/json')
	
