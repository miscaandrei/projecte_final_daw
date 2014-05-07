from ikarus_app.models import *
from django.http import *
import datetime
from models import *

# Create your views here.
def home(request):
    html = "<html><h1 align='center'>Wellcome to </br> Ikarus Project App</h1></html>" 
    return HttpResponse(html)


def d_image(request):
	a=Client.objects.get(nom="Dummy")
	ref = a.avatar
	html = "<html><p> %s. </p></html>" %ref
	return HttpResponse(html)



def image(request):
	a=Client.objects.get(nom="admin")
	ref = a.avatar.read()
	return HttpResponse(ref, content_type="image/png")

