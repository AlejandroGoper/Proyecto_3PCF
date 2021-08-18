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
from matplotlib.cm import RdBu
from PCF import PCF,get_histogram


# Importando archivos

ddd,e_ddd = get_histogram("DDD", "512MPc", 15)
ddr,e_ddr = get_histogram("DDR", "512MPc", 15)
drr,e_drr = get_histogram("DRR", "512MPc", 15)
rrr,e_rrr = get_histogram("RRR", "512MPc", 15)

# Definiendo eje de referencia de la distancia r

bin_index = np.arange(30)
r = (1+bin_index)*(140/30)

r_ = np.linspace(0, 140,30)

r1 = r
r2 = r
r3 = r

# Calculando estimador

_3PCF = PCF(_DDD=ddd, _DDR=ddr, _DRR=drr, _RRR = rrr)
estimador_ss = _3PCF.estimar_3PCF()
error = _3PCF.error_estimador_ss(e_DDD=e_ddd, e_DDR=e_ddr, e_DRR=e_drr, e_RRR = e_rrr)

# Graficando histograma 

# Fijando r3 = 23 MPc -- index = 4
fixed_value_r3 = estimador_ss[:,:,10] 

R1, R2 = np.meshgrid(r_,r_)

fig, ax = plt.subplots()
p = ax.pcolor(R1,R2,fixed_value_r3,cmap=RdBu,vmin=fixed_value_r3.min(), vmax=fixed_value_r3.max())
cb = fig.colorbar(p,ax=ax)