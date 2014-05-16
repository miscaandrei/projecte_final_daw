from django.conf.urls import patterns, include, url
from django.contrib import admin
from ikarus_app.views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'ikarus_app.views.home', name='home'),
    # url(r'^ikarus_base/', include('ikarus_base.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include('marcador.urls')),
    url(r'^image/', 'ikarus_app.views.image', name='image'),
    url(r'^d_image/', 'ikarus_app.views.d_image', name='d_image'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}),
    url(r'^profile/', 'ikarus_app.views.user_profile', name='Profile'),
    url(r'^inventory/', 'ikarus_app.views.user_inventory', name='Inventory'),
    url(r'^json/', 'ikarus_app.views.json_auth_web_service_out', name='JSON'),
    url(r'^json_in/', 'ikarus_app.views.json_auth_web_service_in'),
)


