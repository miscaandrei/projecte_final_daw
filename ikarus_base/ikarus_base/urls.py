from django.conf.urls import patterns, include, url
from django.contrib import admin
from ikarus_app.views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'ikarus_app.views.home', name='home'),
    # url(r'^ikarus_base/', include('ikarus_base.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^image/', 'ikarus_app.views.image', name='image'),
    url(r'^d_image/', 'ikarus_app.views.d_image', name='d_image'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
