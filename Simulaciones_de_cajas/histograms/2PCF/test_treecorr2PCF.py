#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 21:30:30 2021

@author: alejandro_goper

Este script es para realizar test de funcionamiento del codigo trecorr de 
python y generar los histogramas de la 2PCF isotropica.

"""

import numpy as np
import matplotlib.pyplot as plt
import treecorr as tc

# Importando los archivos de data y random

path = "../../"

data = np.genfromtxt(path+"data/data_512MPc_0.dat")
random = np.genfromtxt(path+"random/rand0_512MPc_0.dat")

# Separamos las x, y, z y w en arreglos numpy para procesarlos con treecorr

# DATA
x_d = data[:,0]
y_d = data[:,1]
z_d = data[:,2]
w_d = data[:,3]
# RANDOM
x_r = random[:,0]
y_r = random[:,1]
z_r = random[:,2]
w_r = random[:,3]

"""
==============================================================================
        Probando la funcion de correlacion de dos puntos
==============================================================================
"""

# Catalogamos estos puntos con una clase de treecorr

d_cat = tc.Catalog(x=x_d, y=y_d, z=z_d ,w=w_d)
r_cat = tc.Catalog(x=x_r, y=y_r, z=z_r, w=w_r)

# Procesamos los datos

dd = tc.NNCorrelation(nbins= 30, bin_type= "Linear", metric= "Euclidean", min_sep= 0, max_sep= 140, bin_slop= 0)
dr = tc.NNCorrelation(nbins= 30, bin_type= "Linear", metric= "Euclidean", min_sep= 0, max_sep= 140, bin_slop= 0)
rr = tc.NNCorrelation(nbins= 30, bin_type= "Linear", metric= "Euclidean", min_sep= 0, max_sep= 140, bin_slop= 0)

dd.process(d_cat)
dr.process(d_cat,r_cat)
rr.process(r_cat)

# Calculamos el estimador landy-szaley 

ls, var_ls = dd.calculateXi(rr=rr,dr=dr)

# Graficamos la funcion de correlacion de acuerdo al estimador Landy-Szaley

# Definimos el eje r con el numero de bines

bins = np.arange(30)
bins += 1
bins = (140/30)*bins

# Graficando 

plt.figure(figsize=(20,10))
plt.errorbar(bins,ls*bins*bins,yerr = var_ls*(bins*bins), ecolor="black" ,elinewidth = 3, capsize = 10 ,
             color = "lightgray",fmt = '-o',mfc="red", ms = 10, label="Box: 512 MPc")
plt.legend(fontsize=15,loc="upper left")
plt.grid()
plt.title("2PCF - Dmax: 140 - Bins: 30",fontsize=22)
plt.xlabel(r"$r$ [$MPc$]",fontsize=18)
plt.xticks(fontsize=15)
plt.ylabel(r"$\epsilon_{l-szalay} r^{2}$",fontsize=22)
plt.yticks(fontsize=15)
plt.savefig("treeCorr_2PCF_512MPc_0.png")
plt.show()

