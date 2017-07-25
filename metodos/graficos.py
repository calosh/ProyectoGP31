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
    lista_paises = [
                    ['Argentina', 322], ['Brazil', 21], ['Bolivia', 104], ['Chile', 30], ['Colombia', 731],
                    ['Costa Rica', 23], ['Cuba', 0], ['Ecuador',80], ['El Salvador', 524], ['Guatemala', 620],
                    ['Honduras', 480], ['Mexico', 263], ['Nicaragua', 49], ['Panama', 19], ['Paraguay', 39],
                    ['Peru', 108], ['Puerto Rico', 0], ['Republica Dominicana', 78], ['Uruguay', 22], ['Venezuela', 122]
                    ]



    return lista_paises