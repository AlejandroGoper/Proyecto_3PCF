#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 12:26:21 2021

@author: alejandro_goper

Este script sirve para promediar histogramas de la 3PCF isotropica
y graficar el histograma promedio y la desviación estándar como barra de
error

"""


import numpy as np
import matplotlib.pyplot as plt
from PCF import PCF,get_histogram

from sklearn.decomposition import PCA

# Importando archivos

ddd,e_ddd = get_histogram("DDD", "512MPc", 15)
ddr,e_ddr = get_histogram("DDR", "512MPc", 15)
drr,e_drr = get_histogram("DRR", "512MPc", 15)
rrr,e_rrr = get_histogram("RRR", "512MPc", 15)

# Definiendo eje de referencia de la distancia r

bins = np.arange(30)
bins += 1
bins = (140/30)*bins

# Calculando estimador

_3PCF = PCF(_DDD=ddd, _DDR=ddr, _DRR=drr, _RRR = rrr)
estimador_ss = _3PCF.estimar_3PCF()
error = _3PCF.error_estimador_ss(e_DDD=e_ddd, e_DDR=e_ddr, e_DRR=e_drr, e_RRR = e_rrr)

# Graficando histograma 

pca = PCA(n_components=3)
est_trans = pca.fit_transform(estimador_ss.reshape((30,30*30)))


x_t = est_trans[:,0]
y_t = est_trans[:,1]
z_t = est_trans[:,2]

X,Y,Z,B = np.meshgrid(x_t,y_t,z_t,bins)

fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")
img = ax.scatter(X,Y,Z,c = B,cmap=plt.hot())
fig.colorbar(img)
plt.show()

#contours = plt.contour(X,Y,Z, 3, colors='black')
#plt.clabel(contours, inline=True,fontsize=8)
#plt.imshow(Z)
#plt.colorbar()
#plt.show()










"""
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
"""