#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:27:46 2021

@author: alejandro_goper

Script de pyhton para eliminar los bines negativos de la salida de treecorr
en la  variable v.
"""

import numpy as np

"""
Importamos el archivo de prueba de treecorr: output_TC_1K_30b.dat
"""

archivo = "output_TC_1K_30b.dat"

data = np.loadtxt(archivo)

"""
Separamos por columnas el archivo:
    Solo tomaremos las esenciales para nuestro estudio
"""

r_nom = data[:,0]
u_nom = data[:,1]
v_nom = data[:,2]

zeta = data[:,11]

ddd = data[:,12]
rrr = data[:,13]
drr = data[:,14]
rdd = data[:,15]

"""
Ahora, convertimos el arreglo flatten de Z que entrega la salida de treecorr 
a un array tridimensional de dimensiones (30,30,60)
"""

xi_tc_full = zeta.reshape((30,30,60))


"""
Debemos ahora eliminar los bins negativos de v, 
sabemos que v es simetrico en los bines positivos y negativos, y que por la forma
de v_nom, los primeros 30 bins por cada valor de i,j son negativos y los restantes son
positivos, asi que, debemos eliminar los primeros 30 bins
"""

xi_tc = np.zeros((30,30,30))

for i in range(30):
    for j in range(30):
        for k in range(30):
            xi_tc[i][j][k] = xi_tc_full[i][j][30+k]

"""
La funcion ahora esta lista para ser comparada
"""