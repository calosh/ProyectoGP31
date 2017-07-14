# -*- coding: utf-8 -*-

import csv, operator


with open('extraccioniaLasso2b.csv') as csvarchivo:
    entrada = csv.reader(csvarchivo)
    for reg in entrada:
        print(reg[5])  # Cada línea se muestra como una lista de campos