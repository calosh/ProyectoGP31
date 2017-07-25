# -*- coding: utf-8 -*-
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import datetime
from bs4 import BeautifulSoup

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db import IntegrityError
from django.template.loader import get_template
from django.template import Context

from .models import Tweet

# Tweepy
import tweepy
import time

# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from metodos.scraping_twitter import string_url
from metodos.graficos import mapa1
from metodos.normalizar import eliminar_urls
from metodos.naiveBayes import naive_bayes_classifier


ckey = "wkRHi7BxWy8OzMNd1vuu9yzUU"
csecret = 'Qt8xwKMTY0VswKg5KRJAvpQxH2Oz2mutmh0FiDSnY40wQjLCHY'
atoken = '1048734440-jJr8ZW7JJycCTMtDl90oRLaQO1uX9hHV6d3eGkJ'
asecret = '5aUjQv5tgwjSkvesoeOeRgiAEUBubLct6MqIZjOrFmnYA'
OAUTH_KEYS = {'consumer_key': ckey, 'consumer_secret': csecret, 'access_token_key': atoken,
              'access_token_secret': asecret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth)


def index(request):

    return render(request, 'index.html')


def mapa(request):
    r = mapa1()
    return render(request, 'mapa.html')


def mapa_ajax(request):
    r = mapa1()
    region = ""
    continente = ""
    if request.is_ajax():
        id_region = int(request.GET['id'])
        if id_region == 1:
            region = "013"
            continente = "America Central"
        if id_region == 2:
            region = "029"
            continente = "Caribe"
        if id_region == 3:
            continente = "America del Sur"
            region = "005"

        t = get_template('graficos/mapa_ajax.html')
        html = t.render(Context({'lista': r, 'region': region}))
        html = html + ""
        response = JsonResponse({'mapa': html, 'continente': continente})
        return HttpResponse(response.content)
    else:
        return redirect("/")


def estadisticas(request):
    # Tweets agrupados y contados por fecha
    tweet_group_date = Tweet.objects.extra({'created_at': "date(created_at)"}).values('created_at').annotate(count=Count('id'))
    lista = []
    listaNombreMeses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                        'Octubre', 'Noviembre', 'Diciembre']

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

    # Usuarios que mas publican
    usuarios_publicacion = Tweet.objects.all().values('username').annotate(total=Count('username')).order_by('-total')[0:3]
    lista_usuarios = []
    print usuarios_publicacion
    for i in usuarios_publicacion:
        u = api.get_user(screen_name=i['username'])
        imagen = u.profile_image_url
        imagen = imagen.replace('_normal','_200x200')
        lista_usuarios.append([i['username'], imagen])

    return render(request, 'estadisticas.html', {'listaMesesC':listaMesesC,'tweets_location':tweets_location,
                                                 'listaMesesC20167':listaMesesC20167, 'lista_usuarios':lista_usuarios})


def estadistica1_ajax(request):
    if request.is_ajax():
        id_region = int(request.GET['id'])

        if id_region == 0:
            tweets_location = Tweet.objects.values('location').annotate(total=Count('location')).order_by(
                '-total')[2:7]
            colores = ['#0101DF', '#819FF7', '#BE81F7', '#58FAF4', '#58FA82']

            cont = 0
            tipo = "Reportes"
            for i in tweets_location:
                i['color'] = colores[cont]
                cont = cont + 1

        if id_region == 1:
            tweets_location = Tweet.objects.filter(clasificacion="reporte").values('location').annotate(total=Count('location')).order_by(
                '-total')[1:6]
            colores = ['#0101DF', '#819FF7', '#BE81F7', '#58FAF4', '#58FA82']

            cont = 0
            tipo = "Reportes"
            for i in tweets_location:
                i['color'] = colores[cont]
                cont = cont + 1

        if id_region == 2:
            tweets_location = Tweet.objects.filter(clasificacion="activismo").values('location').annotate(
                total=Count('location')).order_by(
                '-total')[1:6]
            colores = ['#0101DF', '#819FF7', '#BE81F7', '#58FAF4', '#58FA82']

            cont = 0
            tipo = "Activismo"
            for i in tweets_location:
                i['color'] = colores[cont]
                cont = cont + 1

        if id_region == 3:
            tweets_location = Tweet.objects.filter(clasificacion="opinion").values('location').annotate(
                total=Count('location')).order_by(
                '-total')[1:6]
            colores = ['#0101DF', '#819FF7', '#BE81F7', '#58FAF4', '#58FA82']

            cont = 0
            tipo = "Opinion"
            for i in tweets_location:
                i['color'] = colores[cont]
                cont = cont + 1

        t = get_template('graficos/estadistica1_ajax.html')
        html = t.render(Context({'tweets_location': tweets_location, 'tipo':tipo}))
        html = html + ""
        response = JsonResponse({'mapa': html, 'tipo':tipo})
        return HttpResponse(response.content)
    else:
        return redirect("/")


def estadistica2_ajax(request):
    if request.is_ajax():
        id_region = int(request.GET['id'])

        if id_region == 0:
            # Tweets agrupados y contados por fecha
            tweet_group_date = Tweet.objects.extra(
                {'created_at': "date(created_at)"}).values('created_at').annotate(
                count=Count('id'))
            lista = []
            listaNombreMeses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                                'Octubre', 'Noviembre', 'Diciembre']

            listaMeses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in tweet_group_date:
                listaAux = []
                listafecha = i['created_at'].split("-")
                listaAux.append(int(listafecha[0]))
                listaAux.append(int(listafecha[1]) - 1)
                listaAux.append(int(listafecha[2]))
                listaAux.append(int(i["count"]))
                lista.append(listaAux)

                listaMeses[int(listafecha[1]) - 1] = listaMeses[int(listafecha[1]) - 1] + int(i["count"])
            listaMesesC = []

            for i in range(len(listaMeses)):
                listaMesesC.append([listaMeses[i], listaNombreMeses[i]])


        if id_region == 1:
            # Tweets agrupados y contados por fecha
            tweet_group_date = Tweet.objects.filter(clasificacion="reporte").extra(
                {'created_at': "date(created_at)"}).values('created_at').annotate(
                count=Count('id'))
            lista = []
            listaNombreMeses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                                'Octubre', 'Noviembre', 'Diciembre']

            listaMeses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in tweet_group_date:
                listaAux = []
                listafecha = i['created_at'].split("-")
                listaAux.append(int(listafecha[0]))
                listaAux.append(int(listafecha[1]) - 1)
                listaAux.append(int(listafecha[2]))
                listaAux.append(int(i["count"]))
                lista.append(listaAux)

                listaMeses[int(listafecha[1]) - 1] = listaMeses[int(listafecha[1]) - 1] + int(i["count"])
            listaMesesC = []

            for i in range(len(listaMeses)):
                listaMesesC.append([listaMeses[i], listaNombreMeses[i]])

        if id_region == 2:
            # Tweets agrupados y contados por fecha
            tweet_group_date = Tweet.objects.filter(clasificacion="activismo").extra(
                {'created_at': "date(created_at)"}).values('created_at').annotate(
                count=Count('id'))
            lista = []
            listaNombreMeses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                                'Octubre', 'Noviembre', 'Diciembre']

            listaMeses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in tweet_group_date:
                listaAux = []
                listafecha = i['created_at'].split("-")
                listaAux.append(int(listafecha[0]))
                listaAux.append(int(listafecha[1]) - 1)
                listaAux.append(int(listafecha[2]))
                listaAux.append(int(i["count"]))
                lista.append(listaAux)

                listaMeses[int(listafecha[1]) - 1] = listaMeses[int(listafecha[1]) - 1] + int(i["count"])
            listaMesesC = []

            for i in range(len(listaMeses)):
                listaMesesC.append([listaMeses[i], listaNombreMeses[i]])

        if id_region == 3:
            # Tweets agrupados y contados por fecha
            tweet_group_date = Tweet.objects.filter(clasificacion="opinion").extra(
                {'created_at': "date(created_at)"}).values('created_at').annotate(
                count=Count('id'))
            lista = []
            listaNombreMeses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre',
                                'Octubre', 'Noviembre', 'Diciembre']

            listaMeses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in tweet_group_date:
                listaAux = []
                listafecha = i['created_at'].split("-")
                listaAux.append(int(listafecha[0]))
                listaAux.append(int(listafecha[1]) - 1)
                listaAux.append(int(listafecha[2]))
                listaAux.append(int(i["count"]))
                lista.append(listaAux)

                listaMeses[int(listafecha[1]) - 1] = listaMeses[int(listafecha[1]) - 1] + int(i["count"])
            listaMesesC = []

            for i in range(len(listaMeses)):
                listaMesesC.append([listaMeses[i], listaNombreMeses[i]])

        t = get_template('graficos/estadistica2_ajax.html')
        html = t.render(Context({'listaMesesC': listaMesesC}))
        html = html + ""
        response = JsonResponse({'mapa': html})
        return HttpResponse(response.content)
    else:
        return redirect("/")


def estadistica4_ajax(request):
    if request.is_ajax():
        id_region = int(request.GET['id'])

        if id_region == 0:
            # Usuarios que mas publican
            usuarios_publicacion = Tweet.objects.all().values('username').annotate(total=Count('username')).order_by(
                '-total')[0:3]
            lista_usuarios = []
            print usuarios_publicacion
            for i in usuarios_publicacion:
                u = api.get_user(screen_name=i['username'])
                imagen = u.profile_image_url
                imagen = imagen.replace('_normal', '_200x200')
                lista_usuarios.append([i['username'], imagen])

        if id_region == 1:
            # Usuarios que mas publican
            usuarios_publicacion = Tweet.objects.filter(clasificacion='reporte').values('username').annotate(total=Count('username')).order_by(
                '-total')[0:3]
            lista_usuarios = []
            print usuarios_publicacion
            for i in usuarios_publicacion:
                u = api.get_user(screen_name=i['username'])
                imagen = u.profile_image_url
                imagen = imagen.replace('_normal', '_200x200')
                lista_usuarios.append([i['username'], imagen])

        if id_region == 2:
            # Usuarios que mas publican
            usuarios_publicacion = Tweet.objects.filter(clasificacion='activismo').values('username').annotate(total=Count('username')).order_by(
                '-total')[0:3]
            lista_usuarios = []
            print usuarios_publicacion
            for i in usuarios_publicacion:
                u = api.get_user(screen_name=i['username'])
                imagen = u.profile_image_url
                imagen = imagen.replace('_normal', '_200x200')
                lista_usuarios.append([i['username'], imagen])

        if id_region == 3:
            # Usuarios que mas publican
            usuarios_publicacion = Tweet.objects.filter(clasificacion='opinion').values('username').annotate(total=Count('username')).order_by(
                '-total')[0:3]
            lista_usuarios = []
            print usuarios_publicacion
            for i in usuarios_publicacion:
                u = api.get_user(screen_name=i['username'])
                imagen = u.profile_image_url
                imagen = imagen.replace('_normal', '_200x200')
                lista_usuarios.append([i['username'], imagen])

        t = get_template('graficos/estadistica4_ajax.html')
        html = t.render(Context({'lista_usuarios': lista_usuarios}))
        html = html + ""
        response = JsonResponse({'mapa': html})
        return HttpResponse(response.content)
    else:
        return redirect("/")


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


# Obtiene la localizacion del usuario e inserta la localizacion en cada tweet
def get_location(request):
    usuarios = Tweet.objects.values('username').distinct()
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


def naive_bayes(request):
    tweets = Tweet.objects.filter(clasificacion="")[:10000]

    clasificacion = naive_bayes_classifier(tweets)
    cont = 0
    for i in tweets:
        i.clasificacion = clasificacion[cont]
        cont = cont + 1
        i.save()
        print "Guardando: %d" %cont
    print "Se clasificaron: %d" %cont
    return render(request, 'index.html')


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


def extraccion_selenium(request):
    if request.POST:

        url_since = request.POST['fechai']
        url_until = request.POST['fechaf']
        print url_since

        fechai = url_since.split("-")
        fechaf = url_until.split("-")
        for i in range(int(fechai[2]), int(fechaf[2])):  # ciclo desde dia inicial hasta dia final
            browser = webdriver.Chrome()
            url_since_new = "{0}-{1}-{2}".format(fechai[0], fechai[1], i)  # nueva fecha de inicio
            url_until_new = "{0}-{1}-{2}".format(fechai[0], fechai[1], i+1)  # nueva fecha de final
            palabras_clave = request.POST['palabrasc'].split(" ")
            url = string_url(palabras_clave, url_since_new, url_until_new)

            browser.get(url)
            time.sleep(1)

            body = browser.find_element_by_tag_name('body')
            cont = 0
            inner_html = ""

            while True:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)
                try:
                    print "Tweet {0}: {1}".format(cont, body.find_elements_by_class_name('js-tweet-text-container')[cont].text)
                except IndexError:
                    inner_html = body.get_attribute('innerHTML')
                    break
                cont = cont + 1
                if cont == 1000:
                    inner_html = body.get_attribute('innerHTML')
                    break

            html_doc = BeautifulSoup(inner_html, 'html.parser')
            browser.close()

            clase_tweet1 = '''js-stream-item stream-item stream-item
    '''
            # obtenemos los li que contienen el tweet
            tweets = html_doc.find_all('li', class_=clase_tweet1)
            cont = 0

            for j in tweets:
                # obtenemos el primer div del li
                div = j.find('div')
                cont = cont + 1
                print "Tweet: %s" % cont
                try:
                    _timestamp = div.find('span', class_="_timestamp")
                    created_at = _timestamp['data-time-ms']
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


def prueba_ajax(request):
    return render(request, 'ajax.html')


def autor_ajax(request):
    if request.is_ajax():
        x = request.GET['id']
        lista = []
        print "Aqui"
        print type(x)
        if int(x) == 1:
            print "Aqui 2"
            lista = ["Ecuador", "Peru", "Venezuela", "Argentina"]
        
        if int(x) == 2:
            print "Aqui 3"
            lista = ["Paraguay", "Uruguay", "Chile", "Colombia"]
        t = get_template('ajax2.html')
        html = t.render(Context({'lista': lista}))
        html = html +""
        response = JsonResponse({'name':"Carlos", 'x':x, 'p':html})
        return HttpResponse(response.content)
    else:
        return redirect("/")
