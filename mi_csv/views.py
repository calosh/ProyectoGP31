# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse
from django.core.files import File

from .models import Tweet

import urllib
import urllib2
import csv
import codecs
import re

import json
#import simplejson as json

import datetime

from bs4 import BeautifulSoup

from django.db.models import Count


def eliminar_urls(text):
    text = text.replace("https"," https")
    text = text.replace("pic.twitter.com", " https://pic.twitter.com")
    url_patron = re.compile("(?P<url>https?://[^\s]+)")
    text = re.sub(url_patron, '', text)

    return text


def index(request):
    t = Tweet.objects.all()[:100]

    t2 = Tweet.objects.extra({'created_at': "date(created_at)"}).values('created_at').annotate(count=Count('id'))

    print t2

    lista = []
    for i in t2:

        print i['count']

        listaAux = []

        listafecha = i['created_at'].split("-")

        print "esta"
        listaAux.append(int(listafecha[0]))
        listaAux.append(int(listafecha[1]))
        listaAux.append(int(listafecha[2]))
        listaAux.append(int(i["count"]))


        lista.append(listaAux)


    '''
    lista = []
    for i in t:
        listaAux = []


        listaAux.append(i.created_at.year)
        listaAux.append(i.created_at.month)
        listaAux.append(i.created_at.day)

        lista.append(listaAux)
    '''

    return render(request, 'index.html', {'lista':lista})


def index_normalizacion(request):
    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachment; filename=listado.csv'

    #writer = csv.writer(res, delimiter=',', quotechar='"')
    #writer.writerow(['date','username','fullname','responder','retwittear','me gusta','tweet','locate'])

    if request.POST and request.FILES:

        htmlfile = request.FILES['csv_file']

        html_doc = BeautifulSoup(htmlfile, 'html.parser')

        clase_tweet1 = '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
       original-tweet js-original-tweet

       has-cards  has-content
'''

        clase_tweet2 = '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
       original-tweet js-original-tweet

       has-cards dismissible-content has-content
'''

        clase_tweet3 = '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
       original-tweet js-original-tweet

       promoted-tweet has-cards cards-forward
'''

        clase_tweet4 = '''tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content
       original-tweet js-original-tweet


'''

        tweets = html_doc.find_all('div', class_=clase_tweet1)
        print type(tweets)
        tweets = tweets + html_doc.find_all('div', class_=clase_tweet2)
        tweets = tweets + html_doc.find_all('div', class_=clase_tweet3)
        tweets = tweets + html_doc.find_all('div', class_=clase_tweet4)

        print type(tweets)
        #print tweets
        cont = 0

        for i in tweets:

            cont = cont + 1

            print "Tweet: %s" % cont

            try:

                time = i.find('span', class_="_timestamp")
                created_at = time['data-time-ms'] # datetime.datetime.fromtimestamp(created_at/1000.0)
                print created_at
                created_at = datetime.datetime.fromtimestamp(int(created_at)/1000.0)
                print created_at
                fullname = i.find('strong', class_="fullname show-popup-with-id ").get_text()
                username = i.find('span', class_="username u-dir").get_text()
                tweet = i.find('p', class_="TweetTextSize js-tweet-text tweet-text").get_text()

                tweet_id = i['data-tweet-id']


               # print tweet_id['class']

                if len(tweet)<10 or "RT @" in tweet:
                    pass

                tweet = eliminar_urls(tweet)

            except AttributeError:
                pass


            #valoraciones = i.find_all('span', class_="ProfileTweet-actionCountForPresentation")
            #           <span class="ProfileTweet-actionCount" data-tweet-stat-count="1187">
            valoraciones = i.find_all('span', class_="ProfileTweet-actionCount")[0:3]
            print len(valoraciones)


            lista = []
            print valoraciones

            for valoracion in valoraciones:
                # print valoracion
                # print valoracion.find('span', class_="ProfileTweet-actionCountForAria")

                lista.append(valoracion['data-tweet-stat-count'])
                '''
                if valoracion.get_text()=="":
                    lista.append(0)
                else:
                    lista.append(valoracion.get_text())
                '''

            #writer.writerow([date,username, fullname, lista[0], lista[1], lista[2], tweet])
            t1 = Tweet(created_at= created_at,username = username, fullname = fullname, tweet_id =tweet_id, retweet_count = lista[1],
                       text = tweet, location = "", favorite_count = lista[2])

            t1.save()

        #return res

    return render(request, "upload.html", locals())


