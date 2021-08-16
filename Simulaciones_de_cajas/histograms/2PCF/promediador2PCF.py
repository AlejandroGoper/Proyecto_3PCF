#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:26:21 2021

@author: alejandro_goper

Este script sirve para promediar histogramas de la 2PCF isotropica
y graficar el histograma promedio y la desviación estándar como barra de
error

"""


import numpy as np
import matplotlib.pyplot as plt
from PCF import PCF,get_histogram


dd,e_dd = get_histogram("DD", "512MPc", 15)
dr,e_dr = get_histogram("DR", "512MPc", 15)
rr,e_rr = get_histogram("RR", "512MPc", 15)

bins = np.arange(30)
bins += 1
bins = (140/30)*bins

# Calculando estimador

_2PCF = PCF(_DD=dd, _DR=dr, _RR=rr)

est = _2PCF.estimar()
error = _2PCF.error_estimador(E_DD=e_dd, E_DR=e_dr, E_RR=e_rr)

# Graficando histograma 

plt.figure(figsize=(20,10))
plt.errorbar(bins,est*bins*bins,yerr = error*(bins*bins), ecolor="black" ,elinewidth = 3, capsize = 10 ,
             color = "lightgray",fmt = '-o',mfc="red", ms = 10, label="Box: 512 MPc")
plt.legend(fontsize=15,loc="upper left")
plt.grid()
plt.title("2PCF - Dmax: 140 - Bins: 30",fontsize=22)
plt.xlabel("$r$ [$MPc$]",fontsize=18)
plt.xticks(fontsize=15)
plt.ylabel("$\epsilon_{s-szalay} r^{2}$",fontsize=22)
plt.yticks(fontsize=15)
plt.savefig("2PCF_512MPc.png")
plt.show()