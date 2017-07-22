# -*- coding: utf-8 -*-

import nltk
import csv, operator


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


with open('extraccioniaLasso2b.csv') as csvarchivo:
    entrada = csv.reader(csvarchivo)
    for reg in entrada:
        if reg[7]=="1":
            datos.append((reg[5], "positivo"))
        if reg[7] == "-1":
            datos.append((reg[5], "negativo"))
        #print(reg[5])  # Cada línea se muestra como una lista de campos


tweets = []
for (words, sentiment) in datos:
    words_filtered = [e.lower() for e in nltk.word_tokenize(words.decode('utf8')) if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

'''
for t in tweets:
    print(t)
'''
wordFeatures = wordFeatures(bagOfWords(tweets))

training_set = nltk.classify.apply_features(getFeatures, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)

#print(classifier.show_most_informative_features(32))

# http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/

tweet = "La corrupcion en este gobieno ha sido demasiada".decode('utf8')
#print getFeatures(tweet.split())

#print classifier.classify(getFeatures(tweet.split()))


tweet = "Mucha corrupcion de este gobierno".decode('utf8')
#print getFeatures(tweet.split())

print classifier.classify(getFeatures(tweet.split()))

# VivasNosQueremos feminicidio feminicidio NiUnaMenos