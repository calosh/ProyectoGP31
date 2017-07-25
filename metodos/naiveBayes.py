# -*- coding: utf-8 -*-

import nltk
import csv
import os
RUTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def naive_bayes_classifier(lista):

    def bagOfWords(tweets):
        wordsList = []
        for (words, sentiment) in tweets:
            wordsList.extend(words)
        return wordsList


    def wordFeatures(wordList):
        wordList = nltk.FreqDist(wordList)
        wordFeatures = wordList.keys()
        return wordFeatures


    def getFeatures(doc):
        docWords = set(doc)
        feat = {}
        for word in wordFeatures:
            feat['contains(%s)' % word] = (word in docWords)
        return feat

    datos = []
    with open(os.path.join(RUTA, 'metodos/entrenamiento2.csv')) as csvarchivo:
        entrada = csv.reader(csvarchivo)
        for reg in entrada:
            if reg[10]=="activismo":
                #print "Activismo"
                datos.append((reg[7], "activismo"))
            if reg[10] == "reporte":
                #print "Reporte"
                datos.append((reg[7], "reporte"))
            if reg[10] == "opinion":
                #print "Opinion"
                datos.append((reg[7], "opinion"))
            #print(reg[5])  # Cada línea se muestra como una lista de campos



    tweets = []
    for (words, sentiment) in datos:
        words_filtered = [e.lower() for e in nltk.word_tokenize(words.decode('utf8')) if len(e) >= 3]
        tweets.append((words_filtered, sentiment))


    wordFeatures = wordFeatures(bagOfWords(tweets))

    training_set = nltk.classify.apply_features(getFeatures, tweets)

    classifier = nltk.NaiveBayesClassifier.train(training_set)


    # http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/

    #tweet = "Ya no queremos mas feminicidios".decode('utf8')
    #print getFeatures(tweet.split())

    listaClasificacion = []
    cont = 0

    for i in lista:
        listaClasificacion.append(classifier.classify(getFeatures(i.text.split())))
        print cont
        cont = cont + 1

    return listaClasificacion

#naive_bayes(["Ya no queremos mas feminicidios","Basta ya de asesinarnos", 'asesinan a una mujer en mexico'])