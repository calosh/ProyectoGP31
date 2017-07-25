"""ProyectoGP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from mi_csv import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),

    url(r'^calendario$', views.calendario, name="calendario"),
    url(r'^estadisticas$', views.estadisticas, name="estadisticas$"),
    url(r'^location$', views.get_location, name="get_location"),
    url(r'^extraccion$', views.extraccion_selenium, name="extraccion_selenium"),
    url(r'^extraccionia$', views.extraccion_selenium2, name="extraccion_selenium2"),  # exporta a csv
    url(r'^mapa$', views.mapa, name="mapa"),
    url(r'^estadisticas$', views.estadisticas, name="estadisticas"),
    url(r'^naive_bayes$', views.naive_bayes, name="naive_bayes"),

    url(r'^ajax$', views.prueba_ajax, name="prueba_ajax"),
    url(r'^autor-ajax/$', views.autor_ajax, name="autor_ajax"),
    url(r'^mapa-ajax/$', views.mapa_ajax, name="mapa_ajax"),
    url(r'^estadistica1-ajax/$', views.estadistica1_ajax, name="estadistica1_ajax"),
    url(r'^estadistica2-ajax/$', views.estadistica2_ajax, name="estadistica2_ajax"),
    url(r'^estadistica4-ajax/$', views.estadistica4_ajax, name="estadistica4_ajax"),



]
