#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 21:30:30 2021

@author: alejandro_goper

Este script es para realizar test de funcionamiento del codigo trecorr de 
python y generar los histogramas de la 2PCF isotropica.

"""

import numpy as np
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

# Catalogamos estos puntos con una clase de treecorr

d_cat = tc.Catalog(x=x_d, y=y_d, z=z_d ,w=w_d)
r_cat = tc.Catalog(x=x_r, y=y_r, z=z_r, w=w_r)

# Procesamos los datos

dd = tc.NNCorrelation(nbins= 30, bin_type= "Linear", metric= "Euclidean", min_sep= 0, max_sep= 140)
dr = tc.NNCorrelation(nbins= 30, bin_type= "Linear", metric= "Euclidean", min_sep= 0, max_sep= 140)
rr = tc.NNCorrelation(nbins= 30, bin_type= "Linear", metric= "Euclidean", min_sep= 0, max_sep= 140)

dd.process(d_cat)
dr.process(d_cat,r_cat)
rr.process(r_cat)

h_dd = dd.npairs