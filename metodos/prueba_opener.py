# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import urllib
import json
from cmath import polar


def opener(s):

    params = {}
    params['input']=s
    params['kaf']='true'
    params = urllib.urlencode(params)
    f = urllib.urlopen("http://localhost:9293/", params)

    # pos-tagger
    s = f.read()
    params = {}
    params['input']=s
    params['kaf']='true'
    params = urllib.urlencode(params)
    f = urllib.urlopen("http://localhost:9294/", params)

    # polarity-tagger
    s = f.read()
    params = {}
    params['input']=s
    params['kaf']='true'
    params = urllib.urlencode(params)
    f = urllib.urlopen("http://localhost:9295/", params)

    # opinion-detector-basic
    s = f.read()
    params = {}
    params['input']=s
    params['kaf']='true'
    params = urllib.urlencode(params)
    f = urllib.urlopen("http://localhost:9296/", params)

    # kaf2json
    s = f.read()
    params = {}
    params['input']=s
    params['kaf']='true'
    params = urllib.urlencode(params)
    f = urllib.urlopen("http://localhost:9297/", params)

    lista_opener = f.read()
    lista=json.loads(lista_opener)
    #print lista['opinions']
    #print lista['sentiments']
    return lista


twett = """
El pesimista ve dificultad en toda oportunidad. El optimista ve oportunidad en toda dificultad.-Winston Churchill.
"""

s = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <KAF xml:lang="es" version="2.1">
                  <raw>"""+twett+"""</raw>
                </KAF>"""

lista_opener = opener(s)

'''
polaridad = ""
try:
    #print lista_opener['sentiments']
    polaridad = json.dumps(lista_opener['sentiments']).decode('utf-8')
except KeyError:
    polaridad = ""

'''

print lista_opener
