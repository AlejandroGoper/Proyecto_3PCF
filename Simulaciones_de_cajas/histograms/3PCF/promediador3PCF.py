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
from matplotlib.colors import Normalize

# Importando archivos

ddd,e_ddd = get_histogram("DDD", "512MPc", 15)
ddr,e_ddr = get_histogram("DDR", "512MPc", 15)
drr,e_drr = get_histogram("DRR", "512MPc", 15)
rrr,e_rrr = get_histogram("RRR", "512MPc", 15)


"""
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
"""

"""

Graficando cortes de la 3PCF:
    
    - La 3PCF se grafica en 4 dimensiones r (el eje de la dmax) y las 3 dim del resultado de xi o el estimador
    - Xi(r1,r2,r3) si nbins= 30 tendra dimension Xi(30,30,30)
    - Fijamos r3 a algun valor, es decir, digamos 10 XI(r1,r2,10) y resultara una matriz de dimensiones 30x30
    - Graficamos esta matriz con imshow de python si solo no quiero mapear los ejes, y con pcolormesh si quiero mapear los ejes.
    



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
fixed_value_r3 = estimador_ss[:,:,4] 

R1, R2 = np.meshgrid(r_,r_)

#fig, ax = plt.subplots()

# Opcion graica 1
#plt.imshow(fixed_value_r3, origin="lower",cmap=RdBu, interpolation="bilinear",norm=norm, vmin=-1,vmax=1)
#plt.colorbar()
#plt.show()

# Opcion grafica 2
#p = plt.pcolormesh(R1,R2,fixed_value_r3,cmap=RdBu, vmin=-1,vmax=1) 
#cb = fig.colorbar(p,ax=ax)

# Opcion grafica 3


#Vamos a aplanar todo el array de la 3PCF para poderlo graficar en 2D


aplanado_3PCF = estimador_ss.flatten()



# Graficando 

plt.figure(figsize=(20,10))
#plt.errorbar(bins,ls*bins*bins,yerr = var_ls*(bins*bins), ecolor="black" ,elinewidth = 3, capsize = 10 ,
#             color = "lightgray",fmt = '-o',mfc="red", ms = 10, label="Box: 512 MPc")
plt.plot(np.log(np.abs(aplanado_3PCF)), label="3PCF-Flattened")
plt.legend(fontsize=15,loc="upper right")
plt.grid()
plt.ylim([-10,10])
#plt.title("2PCF - Dmax: 140 - Bins: 30",fontsize=22)
plt.xlabel(r"Bin",fontsize=18)
plt.xticks(fontsize=15)
plt.ylabel(r"$\epsilon$",fontsize=22)
plt.yticks(fontsize=15)
plt.savefig("treeCorr_3PCF_512MPc_0.png")
plt.show()

"""

"""
Mapeo a las variables de TreeCorr

r = d2
u = d3 / d2
v = (d1 - d2)/d3

Vamos a mapear los histogramas directamente.
"""

# Construimos unas histogramas vacios para las nuevas variables, r,u,v

ddd_mapeo = np.zeros((30,30,30))
rrr_mapeo = np.zeros((30,30,30))
drr_mapeo = np.zeros((30,30,30))
rdd_mapeo = np.zeros((30,30,30))

# Recorremos el histograma clasico respetando la jerarquia de treccor d1>d2>d3

c = 140/30
# Esto es porque para las variables u,v el valor maximo es 1, y nbins = 30
c_u = 1/30
c_v = c_u

for i in range(29):
    for j in range(i):
        for k in range(j):
            # Guardamos la contribucion del bin pivote en nuestro histograma
            ddd_value = ddd[i][j][k]
            rrr_value = rrr[i][j][k]
            drr_value = drr[i][j][k]
            rdd_value = ddr[i][j][k]
            print(f"i={i}, j={j}, k={k}")
            # Calculamos las nuevas variables
            r = c*(i+1)
            u = (k+1)/(j+1)
            v = (i-j)/(k+1)
            print(f"r={r}, u={u}, v={v}")
            # Calculamos ahora el indice que le corresponde en el array de nuevas variables
            i_r = int(r/c)
            i_u = int(u/c_u)
            i_v = int(v/c_v)
            print(f"i_r = {i_r}, i_u= {i_u}, i_v= {i_v}")
            



