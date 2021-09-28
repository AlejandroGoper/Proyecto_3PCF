#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 13:12:06 2021

@author: alejandro_goper

Este script es para realizar test de funcionamiento del codigo trecorr de 
python y generar los histogramas de la 3PCF isotropica.


"""


import numpy as np
import matplotlib.pyplot as plt
import treecorr as tc
from matplotlib.colors import Normalize
from matplotlib.cm import RdBu
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
        Probando la funcion de correlacion de tres puntos
==============================================================================
"""

# Catalogamos estos puntos con una clase de treecorr

d_cat = tc.Catalog(x=x_d[:1000], y=y_d[:1000], z=z_d[:1000] ,w=w_d[:1000])
r_cat = tc.Catalog(x=x_r[:1000], y=y_r[:1000], z=z_r[:1000], w=w_r[:1000])


# Procesamos los datos

ddd = tc.NNNCorrelation(nbins= 30, bin_type= "LogRUV", metric= "Euclidean", min_sep= 1, max_sep=140, bin_slop= 0, nubins=30,nvbins=30)
rdd = tc.NNNCorrelation(nbins= 30, bin_type= "LogRUV", metric= "Euclidean", min_sep= 1, max_sep=140, bin_slop= 0, nubins=30,nvbins=30)
drr = tc.NNNCorrelation(nbins= 30, bin_type= "LogRUV", metric= "Euclidean", min_sep= 1, max_sep=140, bin_slop= 0, nubins=30,nvbins=30)
rrr = tc.NNNCorrelation(nbins= 30, bin_type= "LogRUV", metric= "Euclidean", min_sep= 1, max_sep=140, bin_slop= 0, nubins=30,nvbins=30)

ddd.process(d_cat)
rrr.process(r_cat)
drr.process(d_cat,r_cat)
rdd.process(r_cat,d_cat)

ddd.write('output_TC_1K_30b.dat',rrr,drr,rdd)
# Calculamos el estimador zeta 

zeta, var_zeta = ddd.calculateZeta(rrr=rrr,drr=drr,rdd=rdd)

# Graficamos la funcion de correlacion de acuerdo al estimador Landy-Szaley


"""

# Graficando histograma 
class MidpointNormalize(Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

norm = MidpointNormalize(midpoint=0)



# Fijando r3 = 23 MPc -- index = 4
fixed_value_r3 = zeta[:,:,4] 

#R1, R2 = np.meshgrid(r_,r_)

fig, ax = plt.subplots()

# Opcion graica 1
plt.imshow(fixed_value_r3, origin="lower",cmap=RdBu, interpolation="bilinear",norm=norm, vmin=-1,vmax=1)
plt.colorbar()
plt.show()
"""