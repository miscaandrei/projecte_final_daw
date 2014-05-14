from ikarus_app.models import *
from django.http import *
import datetime
from models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.contrib import auth


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
	return render( request, "profile.html", {"ref_client": client.ref_client, "Nom":client.nom ,"Cognoms":client.cognoms, "rating":client.rating, "location":client.location}) #aixo ja funciona

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