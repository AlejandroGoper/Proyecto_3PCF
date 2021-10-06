#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 20:30:03 2021

@author: alejandro_goper

Script para comparar histogramas.

"""
from numpy import genfromtxt,zeros,log,arange
from modulo_preparacion_tc import eliminar_v_negativos

import matplotlib.pyplot as plt

ddd_tc, rrr_tc, drr_tc, rdd_tc = eliminar_v_negativos("output_TC_1K_80b.dat",80)

ddd = genfromtxt("DDD/DDDiso_data_1K_80b.dat").reshape(80,80,80)
rrr = genfromtxt("RRR/RRRiso_rand0_1K_80b.dat").reshape(80,80,80)
drr = genfromtxt("DRR/DRRiso_rand0_1K_80b.dat").reshape(80,80,80)
rdd = genfromtxt("DDR/DDRiso_rand0_1K_80b.dat").reshape(80,80,80)

# Mapeando


"""
Mapeo a las variables de TreeCorr

r = d2
u = d3 / d2
v = (d1 - d2)/d3

Vamos a mapear los histogramas directamente.
"""

# Construimos unas histogramas vacios para las nuevas variables, r,u,v

ddd_mapeo = zeros((80,80,80))
rrr_mapeo = zeros((80,80,80))
drr_mapeo = zeros((80,80,80))
rdd_mapeo = zeros((80,80,80))

# Recorremos el histograma clasico respetando la jerarquia de treccor d1>d2>d3

c = 140/80
# Esto es porque para las variables u,v el valor maximo es 1, y nbins = 30
c_u = 1/80
c_v = c_u
c_r = log(140)/80
# Funcion para verificar si un triplete es un triangulo:

def es_triangulo(d1,d2,d3):
    if ((d1+d2>d3) and (d1+d3>d2) and (d2+d3>d1) ):
        return True
    else:
        return False


for i in range(79):
    for j in range(i):
        for k in range(j):
            # Guardamos la contribucion del bin pivote en nuestro histograma
            ddd_value = ddd[i][j][k]
            rrr_value = rrr[i][j][k]
            drr_value = drr[i][j][k]
            rdd_value = rdd[i][j][k]
            #print(f"i={i}, j={j}, k={k}")
            if(es_triangulo(c*i, c*j, c*k)):
                # Calculamos las nuevas variables
                r = log(c*(i+1))
                u = (k+1)/(j+1)
                v = (i-j)/(k+1)
                #print(f"r={r}, u={u}, v={v}")
                # Calculamos ahora el indice que le corresponde en el array de nuevas variables
                i_r = int(r/c_r)
                i_u = int(u/c_u)
                i_v = int(v/c_v)
                #print(f"i_r = {i_r}, i_u= {i_u}, i_v= {i_v}")
                ddd_mapeo[i_r][i_u][i_v] += ddd_value
                rrr_mapeo[i_r][i_u][i_v] += rrr_value
                drr_mapeo[i_r][i_u][i_v] += drr_value
                rdd_mapeo[i_r][i_u][i_v] += rdd_value




# Graficando histogramas

ddd_flatten_tc = ddd_tc.flatten()
rrr_flatten_tc = rrr_tc.flatten()
drr_flatten_tc = drr_tc.flatten()
rdd_flatten_tc = rdd_tc.flatten()

ddd_flatten = ddd_mapeo.flatten()
drr_flatten = drr_mapeo.flatten()
rdd_flatten = rdd_mapeo.flatten()
rrr_flatten = rrr_mapeo.flatten()


def comparar(hist_tc, hist, nombre):
    fig, axs = plt.subplots(2,1, sharex=True)

    fig.suptitle("Comparacion de histogramas 3PCF - 80 bins")


    axs[0].plot(hist_tc)
    axs[0].set_title(nombre+r"$_{TreeCorr}$")


    axs[1].plot(hist)
    axs[1].set_title(nombre)
    
    plt.tight_layout()
    plt.savefig(nombre+"_comparacion_80b.png")
    plt.show()
    
comparar(hist_tc=ddd_flatten_tc, hist=ddd_flatten, nombre="DDD")
comparar(hist_tc=rrr_flatten_tc, hist=rrr_flatten, nombre="RRR")
comparar(hist_tc=rdd_flatten_tc, hist=rdd_flatten, nombre="RDD")
comparar(hist_tc=drr_flatten_tc, hist=drr_flatten, nombre="DRR")
