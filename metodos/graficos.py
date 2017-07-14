from mi_csv.models import Tweet
from django.db.models import Count


def calendario():
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

    return {'lista': lista, 'listaMesesC':listaMesesC,'tweets_location':tweets_location}


def mapa1():
    lista_paises = ['Argentina', 'Brazil', 'Bolivia', 'Chile', 'Colombia', 'Costa Rica', 'Cuba',
                    'Ecuador', 'El Salvador', 'Guatemala', 'Honduras', 'Mexico', 'Nicaragua', 'Panama',
                    'Paraguay', 'Peru', 'Puerto Rico', 'Peru', 'Republica Dominicana', 'Uruguay', 'Venezuela'
                    ]

    paises =[]
    for i in lista_paises:
        paisesT = Tweet.objects.filter(location=i).count()
        paises.append([i, paisesT])

    return paises