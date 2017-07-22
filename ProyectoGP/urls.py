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
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),

    url(r'^calendario$', views.calendario, name="calendario"),
    url(r'^estadisticas$', views.estadisticas, name="estadisticas$"),
    url(r'^normalizar.csv$', views.index_normalizacion, name="index_normalizacion"),
    url(r'^location$', views.get_location, name="get_location"),
    url(r'^extraccion$', views.extraccion_selenium3, name="extraccion_selenium3"),
    url(r'^extraccionia$', views.extraccion_selenium2, name="extraccion_selenium2"),
    url(r'^mapa', views.mapa, name="mapa"),
]
