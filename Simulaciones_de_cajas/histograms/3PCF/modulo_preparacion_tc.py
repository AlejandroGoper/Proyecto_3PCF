#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 17:27:46 2021

@author: alejandro_goper

Script de pyhton para eliminar los bines negativos de la salida de treecorr
en la  variable v.
"""

from numpy import loadtxt, zeros

"""
Este modulo sirve para eliminar los valores de los bines negativos de v en 
la funcion de correlacion dada por treecorr. 

Argumentos:
    archivo: nombre del archivo de salida de treecorr extension ".dat"
    nbin: numero de bins

Devuelve:
    la funcion de correlacion xi con solo bines de v positivos.
"""

def eliminar_v_negativos(archivo,nbins):
    
    """
    Importamos el archivo de prueba de treecorr: output_TC_1K_30b.dat
    """    
    data = loadtxt(archivo)
    
    """
    Separamos por columnas el archivo:
        Solo tomaremos las esenciales para nuestro estudio
    """
    
    #r_nom = data[:,0]
    #u_nom = data[:,1]
    #v_nom = data[:,2]
    
    zeta = data[:,11]
    
    #ddd = data[:,12]
    #rrr = data[:,13]
    #drr = data[:,14]
    #rdd = data[:,15]
    
    """
    Ahora, convertimos el arreglo flatten de Z que entrega la salida de treecorr 
    a un array tridimensional de dimensiones (nbins,nbins,2*nbins)
    """
    
    xi_tc_full = zeta.reshape((nbins,nbins,2*nbins))
    
    
    """
    Debemos ahora eliminar los bins negativos de v, 
    sabemos que v es simetrico en los bines positivos y negativos, y que por la forma
    de v_nom, los primeros 30 bins por cada valor de i,j son negativos y los restantes son
    positivos, asi que, debemos eliminar los primeros 30 bins
    """
    
    xi_tc = zeros((nbins,nbins,nbins))
    
    for i in range(nbins):
        for j in range(nbins):
            for k in range(nbins):
                xi_tc[i][j][k] = xi_tc_full[i][j][nbins+k]
    
    return xi_tc