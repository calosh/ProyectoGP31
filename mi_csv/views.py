# -*- coding: utf-8 -*-
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import datetime
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse
from metodos.normalizar import eliminar_urls
from django.db.models import Count
from django.db import IntegrityError

from .models import Tweet

from metodos.graficos import mapa1

# Tweepy
import tweepy
import time

ckey = "wkRHi7BxWy8OzMNd1vuu9yzUU"
csecret = 'Qt8xwKMTY0VswKg5KRJAvpQxH2Oz2mutmh0FiDSnY40wQjLCHY'
atoken = '1048734440-jJr8ZW7JJycCTMtDl90oRLaQO1uX9hHV6d3eGkJ'
asecret = '5aUjQv5tgwjSkvesoeOeRgiAEUBubLct6MqIZjOrFmnYA'
OAUTH_KEYS = {'consumer_key': ckey, 'consumer_secret': csecret, 'access_token_key': atoken,
              'access_token_secret': asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)


def index(request):
    r = mapa1()
    return render(request, 'index.html',{'paises':r})


def estadisticas(request):
    # Tweets agrupados y contados por fecha
    tweet_group_date = Tweet.objects.extra({'created_at': "date(created_at)"}).values('created_at').annotate(count=Count('id'))
    lista = []
    listaNombreMeses = ['Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre',
                        'Octubre','Noviembre','Diciembre']

    listaMeses = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in tweet_group_date:
        listaAux = []
        listafecha = i['created_at'].split("-")
        listaAux.append(int(listafecha[0]))
        listaAux.append(int(listafecha[1]) - 1)
        listaAux.append(int(listafecha[2]))
        listaAux.append(int(i["count"]))
        lista.append(listaAux)

        # Meses
        print int(listafecha[1]) - 1

        listaMeses[int(listafecha[1]) - 1] = listaMeses[int(listafecha[1]) - 1] + int(i["count"])
    print listaMeses
    listaMesesC = []

    for i in range(len(listaMeses)):
        listaMesesC.append([listaMeses[i], listaNombreMeses[i]])

    tweets_location = Tweet.objects.all().values('location').annotate(total=Count('location')).order_by('-total')[2:7]
    colores = ['#0101DF','#819FF7','#BE81F7','#58FAF4','#58FA82']
    cont = 0
    for i in tweets_location:

        i['color'] = colores[cont]
        cont = cont + 1

    listaMesesC20167 = listaMesesC
    listaInv = [6056, 4056, 7034]
    cont = 0
    for i in listaMesesC20167:
        if cont>=3:
            i.append(0)
        else:
            i.append(listaInv[cont])
        cont = cont +1
    #print listaMesesC20167
    return render(request, 'estadisticas.html', {'listaMesesC':listaMesesC,'tweets_location':tweets_location, 'listaMesesC20167':listaMesesC20167})

def calendario(request):
    # Tweets agrupados y contados por fecha
    tweet_group_date = Tweet.objects.extra({'created_at': "date(created_at)"}).values('created_at').annotate(count=Count('id')).filter(created_at__year=2017)
    lista = []

    for i in tweet_group_date:
        listaAux = []
        listafecha = i['created_at'].split("-")
        listaAux.append(int(listafecha[0]))
        listaAux.append(int(listafecha[1]) - 1)
        listaAux.append(int(listafecha[2]))
        listaAux.append(int(i["count"]))
        lista.append(listaAux)

        # Meses
        print int(listafecha[1]) - 1

    return render(request, 'calendario.html', {'lista': lista})


def mapa(request):
    r = mapa1()
    return render(request, 'mapa.html', {'paises': r})

def index_normalizacion(request):
    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachment; filename=listado.csv'

    # writer = csv.writer(res, delimiter=',', quotechar='"')
    # writer.writerow(['date','username','fullname','responder','retwittear','me gusta','tweet','locate'])

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
        # print tweets
        cont = 0

        for i in tweets:

            cont = cont + 1

            print "Tweet: %s" % cont

            try:

                time = i.find('span', class_="_timestamp")
                created_at = time['data-time-ms']  # datetime.datetime.fromtimestamp(created_at/1000.0)
                print created_at
                created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000.0)
                print created_at
                fullname = i.find('strong', class_="fullname show-popup-with-id ").get_text()
                username = i.find('span', class_="username u-dir").get_text()
                tweet = i.find('p', class_="TweetTextSize js-tweet-text tweet-text").get_text()

                tweet_id = i['data-tweet-id']

                # print tweet_id['class']

                if len(tweet) < 10 or "RT @" in tweet:
                    pass

                tweet = eliminar_urls(tweet)

            except AttributeError:
                pass

            # valoraciones = i.find_all('span', class_="ProfileTweet-actionCountForPresentation")
            #           <span class="ProfileTweet-actionCount" data-tweet-stat-count="1187">
            valoraciones = i.find_all('span', class_="ProfileTweet-actionCount")[0:3]
            #print len(valoraciones)

            lista = []
            #print valoraciones

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

            # writer.writerow([date,username, fullname, lista[0], lista[1], lista[2], tweet])
            t1 = Tweet(created_at=created_at, username=username, fullname=fullname, tweet_id=tweet_id,
                       retweet_count=lista[1],
                       text=tweet, location="", favorite_count=lista[2])

            try:
                t1.save()
            except IntegrityError:
                print "Ya existe"

                # return res

    return render(request, "upload.html", locals())


def get_location(request):
    usuarios = Tweet.objects.values('username').distinct()
    # usuarios = Tweet.objects.filter(location="")
    cont = 0

    for usuario in usuarios:
        obj = Tweet.objects.filter(username=usuario['username'], location="")

        # Si no hay objetos en la consulta, se continua con el siguiente usuario
        if not obj:
            print "paso"
            continue

        try:
            print usuario
            u = api.get_user(screen_name=usuario['username'])
        except tweepy.TweepError:
            print usuario['username']
            print "Error"
            continue

        for i in obj:
            if u.location == "" or len(u.location) == 0:
                i.location = "S/L"
                i.followers = u.followers_count
            else:
                print "Aqui"
                i.location = u.location
                i.followers = u.followers_count
                print u.location

            print i.id

            i.save()

        print cont
        cont = cont + 1
        '''
        if cont >= 40:
            time.sleep(60*1)
            cont = 0
        '''
    return render(request, 'prueba.html')


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from metodos.scraping_twitter import string_url, string_url2

def extraccion_selenium(request):

    if request.POST:
        browser = webdriver.Chrome()
        url_since = request.POST['fechai']
        url_until = request.POST['fechaf']
        print url_since
        print url_until
        palabras_clave = request.POST['palabrasc'].split(" ")
        #palabras_clave = ['femicidio', 'feminicidio', 'niunamenos']

        url = string_url(palabras_clave,url_since,url_until)

        #url = "https://twitter.com/search?l=es&q=femicidio%20since%3A2016-01-01%20until%3A2016-01-02&src=typd&lang=es"

        browser.get(url)
        time.sleep(1)

        body = browser.find_element_by_tag_name('body')
        cont = 0
        innerHTML = ""

        while True:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)
            try:
                print "Tweet {0}: {1}".format(cont, body.find_elements_by_class_name('js-tweet-text-container')[cont].text)
                #print body.find_elements_by_class_name('js-tweet-text-container')[cont].text
            except IndexError:
                innerHTML = body.get_attribute('innerHTML')
                break
            cont = cont + 1
            if cont == 1000:
                innerHTML = body.get_attribute('innerHTML')
                break

        #print innerHTML
        html_doc = BeautifulSoup(innerHTML, 'html.parser')
        #print html_doc
        browser.close()

        clase_tweet1 = '''js-stream-item stream-item stream-item
'''
        # obtenemos los li que contienen el tweet
        tweets = html_doc.find_all('li', class_=clase_tweet1)
        cont = 0

        for i in tweets:
            # obtenemos el primer div del li
            div = i.find('div')
            cont = cont + 1
            print "Tweet: %s" % cont
            try:
                timeT = div.find('span', class_="_timestamp")
                created_at = timeT['data-time-ms']  # datetime.datetime.fromtimestamp(created_at/1000.0)
                created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000.0)
                fullname = div.find('strong', class_="fullname show-popup-with-id ").get_text()
                username = div.find('span', class_="username u-dir").get_text()
                tweet = div.find('p', class_="TweetTextSize js-tweet-text tweet-text").get_text()
                tweet_id = div['data-tweet-id']

                if len(tweet) < 10 or "RT @" in tweet:
                    pass

                tweet = eliminar_urls(tweet)

            except AttributeError:
                pass

            # valoraciones = i.find_all('span', class_="ProfileTweet-actionCountForPresentation")
            #           <span class="ProfileTweet-actionCount" data-tweet-stat-count="1187">
            valoraciones = div.find_all('span', class_="ProfileTweet-actionCount")[0:3]
            lista = []

            for valoracion in valoraciones:
                lista.append(valoracion['data-tweet-stat-count'])

            t1 = Tweet(created_at=created_at, username=username, fullname=fullname, tweet_id=tweet_id,
                       retweet_count=lista[1],
                       text=tweet, location="", favorite_count=lista[2])

            try:
                t1.save()
            except IntegrityError:
                print "Ya existe"

    return render(request, "upload_selenium.html", locals())


# IA Export csv
def extraccion_selenium2(request):
    res = HttpResponse(content_type='text/csv')
    res['Content-Disposition'] = 'attachment; filename=listado.csv'

    writer = csv.writer(res, delimiter=',', quotechar='"')

    '''
    t1 = Tweet(created_at=created_at, username=username, fullname=fullname, tweet_id=tweet_id,
                       retweet_count=lista[1],
                       text=tweet, location="", favorite_count=lista[2])
    '''
    writer.writerow(['date','username','fullname','tweet_id','retweet_count','tweet','favorite_count'])

    if request.POST:
        browser = webdriver.Chrome()
        url_since = request.POST['fechai']
        url_until = request.POST['fechaf']
        print url_since
        print url_until
        palabras_clave = request.POST['palabrasc'].split(" ")

        url = string_url(palabras_clave,url_since,url_until)

        browser.get(url)
        time.sleep(1)

        body = browser.find_element_by_tag_name('body')
        cont = 0
        innerHTML = ""

        while True:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
            try:
                print "Tweet {0}: {1}".format(cont, body.find_elements_by_class_name('js-tweet-text-container')[cont].text)
                #print body.find_elements_by_class_name('js-tweet-text-container')[cont].text
            except IndexError:
                innerHTML = body.get_attribute('innerHTML')
                break
            cont = cont + 1

        #print innerHTML
        html_doc = BeautifulSoup(innerHTML, 'html.parser')
        #print html_doc
        browser.close()

        clase_tweet1 = '''js-stream-item stream-item stream-item
'''
        # obtenemos los li que contienen el tweet
        tweets = html_doc.find_all('li', class_=clase_tweet1)
        cont = 0

        for i in tweets:
            # obtenemos el primer div del li
            div = i.find('div')
            cont = cont + 1
            print "Tweet: %s" % cont
            try:
                timeT = div.find('span', class_="_timestamp")
                created_at = timeT['data-time-ms']  # datetime.datetime.fromtimestamp(created_at/1000.0)
                created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000.0)
                fullname = div.find('strong', class_="fullname show-popup-with-id ").get_text()
                username = div.find('span', class_="username u-dir").get_text()
                tweet = div.find('p', class_="TweetTextSize js-tweet-text tweet-text").get_text()
                tweet_id = div['data-tweet-id']

                if len(tweet) < 10 or "RT @" in tweet:
                    pass

                tweet = eliminar_urls(tweet)

            except AttributeError:
                pass

            # valoraciones = i.find_all('span', class_="ProfileTweet-actionCountForPresentation")
            #           <span class="ProfileTweet-actionCount" data-tweet-stat-count="1187">
            valoraciones = div.find_all('span', class_="ProfileTweet-actionCount")[0:3]
            lista = []

            for valoracion in valoraciones:
                lista.append(valoracion['data-tweet-stat-count'])

            writer.writerow([created_at, username, fullname, tweet_id, lista[1], tweet, lista[2]])

            '''
            t1 = Tweet(created_at=created_at, username=username, fullname=fullname, tweet_id=tweet_id,
                       retweet_count=lista[1],
                       text=tweet, location="", favorite_count=lista[2])

            try:
                t1.save()
            except IntegrityError:
                print "Ya existe"
            '''
        return res

    return render(request, "upload_selenium.html", locals())


def extraccion_selenium3(request):

    if request.POST:
        url_since = request.POST['fechai']
        url_until = request.POST['fechaf']
        print url_since

        fechai = url_since.split("-")
        fechaf = url_until.split("-")
        for i in range(int(fechai[2]), int(fechaf[2])): # ciclo desde dia inicial hasta dia final
            browser = webdriver.Chrome()
            url_since_new = "{0}-{1}-{2}".format(fechai[0],fechai[1], i) # nueva fecha de inicio
            url_until_new = "{0}-{1}-{2}".format(fechai[0],fechai[1], i+1) # nueva fecha de final
            palabras_clave = request.POST['palabrasc'].split(" ")
            url = string_url(palabras_clave,url_since_new,url_until_new)

            browser.get(url)
            time.sleep(1)

            body = browser.find_element_by_tag_name('body')
            cont = 0
            innerHTML = ""

            while True:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                try:
                    print "Tweet {0}: {1}".format(cont, body.find_elements_by_class_name('js-tweet-text-container')[cont].text)
                except IndexError:
                    innerHTML = body.get_attribute('innerHTML')
                    break
                cont = cont + 1
                if cont == 1000:
                    innerHTML = body.get_attribute('innerHTML')
                    break

            html_doc = BeautifulSoup(innerHTML, 'html.parser')
            browser.close()

            clase_tweet1 = '''js-stream-item stream-item stream-item
    '''
            # obtenemos los li que contienen el tweet
            tweets = html_doc.find_all('li', class_=clase_tweet1)
            cont = 0

            for i in tweets:
                # obtenemos el primer div del li
                div = i.find('div')
                cont = cont + 1
                print "Tweet: %s" % cont
                try:
                    timeT = div.find('span', class_="_timestamp")
                    created_at = timeT['data-time-ms']  # datetime.datetime.fromtimestamp(created_at/1000.0)
                    created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000.0)
                    fullname = div.find('strong', class_="fullname show-popup-with-id ").get_text()
                    username = div.find('span', class_="username u-dir").get_text()
                    tweet = div.find('p', class_="TweetTextSize js-tweet-text tweet-text").get_text()
                    tweet_id = div['data-tweet-id']

                    if len(tweet) < 10 or "RT @" in tweet:
                        continue

                    tweet = eliminar_urls(tweet)

                except AttributeError:
                    pass

                valoraciones = div.find_all('span', class_="ProfileTweet-actionCount")[0:3]
                lista = []

                for valoracion in valoraciones:
                    lista.append(valoracion['data-tweet-stat-count'])

                t1 = Tweet(created_at=created_at, username=username, fullname=fullname, tweet_id=tweet_id,
                           retweet_count=lista[1],
                           text=tweet, location="", favorite_count=lista[2])

                try:
                    t1.save()
                except IntegrityError:
                    print "Ya existe"

    return render(request, "upload_selenium.html", locals())