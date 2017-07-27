
'''
palabras_clave = ['femicidio','feminicidio','niunamenos']

palabras_clave_url = ""

for i in palabras_clave:
    if len(palabras_clave) > 1:
        if i == palabras_clave[len(palabras_clave)-1]:
            palabras_clave_url = palabras_clave_url + "{0}%20".format(i)
        else:
            palabras_clave_url = palabras_clave_url+"{0}%20OR%20".format(i)
    else:
        palabras_clave_url = "{0}%20".format(i)

#print palabras_clave_url

url_since = "2016-01-01"
url_until = "2016-01-02"

#url = "https://twitter.com/search?l=es&q=femicidio%20OR%20feminicidio%20since%3A2017-05-01%20until%3A2017-05-03&src=typd&lang=es"
url2 = "https://twitter.com/search?l=es&q={0}since%3A{1}%20until%3A{2}&src=typd&lang=es"\
    .format(palabras_clave_url,url_since, url_until)

#print url
print url2
'''

def string_url(palabras_clave,url_since,url_until):


    palabras_clave_url = ""
    for i in palabras_clave:
        if len(palabras_clave) > 1:
            if i == palabras_clave[len(palabras_clave) - 1]:
                palabras_clave_url = palabras_clave_url + "{0}%20".format(i)
            else:
                palabras_clave_url = palabras_clave_url + "{0}%20OR%20".format(i)
        else:
            palabras_clave_url = "{0}%20".format(i)


    # url = "https://twitter.com/search?l=es&q=femicidio%20OR%20feminicidio%20since%3A2017-05-01%20until%3A2017-05-03&src=typd&lang=es"
    url2 = ("https://twitter.com/search?l=&q={0}since%3A{1}%20until%3A{2}&src=typd&lang=es"
            .format(palabras_clave_url, url_since, url_until))

    return url2
