# -*- coding: utf-8 -*-

import csv, operator


with open('tweetsFeminicidios.csv') as csvarchivo:
    entrada = csv.reader(csvarchivo)
    for reg in entrada:
        print(reg)  # Cada línea se muestra como una lista de campos