#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 14:24:26 2021

@author: alejandro_goper

Clase para propagacion de errores de la 2PCF isotropica

Szapudi & Szalay - Estimator
"""

from numpy import ones,sqrt,genfromtxt,mean,std

class PCF:
    # Metodo constructor
    def __init__(self,_DD,_DR,_RR):
        # Atributos de clase
        self.DD = _DD
        self.DR = _DR
        self.RR = _RR
        
    """
        Se utiliza el estimador de Szapudi & Szalay
    """
    def estimar(self):
        one = ones(len(self.DD))
        est = self.DD/self.RR -2*self.DR/self.RR + one
        return est
    
    """
        Propagacion del error 
    """
    def error_estimador(self, E_DD, E_DR, E_RR):
        error2 = (self.partial_dd()*E_DD)**2 + (self.partial_dr()*E_DR)**2 + (self.partial_rr()*E_RR)**2
        error = sqrt(error2)
        return error
    
    def partial_dd(self):
        return ones(len(self.DD))/self.RR        # 1/rr
    
    def partial_dr(self):
        return -2*self.partial_dd() # -2/rr
    
    def partial_rr(self):
        x = self.partial_dd()
        x2 = x*x 
        return -self.DD*x2 + 2*self.DR*x2  # -dd/(rr)**2 +2dr/(rr)**2
        

def get_histogram(name,box,n_files):
    tensor = []
    if(name == "DD"):
        carpeta = name+"/"
        archivo_prefijo = name+"iso_data_" + box + "_"
    elif(name == "DR" or name == "RR"):
        carpeta = name+"/"
        archivo_prefijo = name+"iso_rand0_" + box + "_"

    for i in range(n_files):
        x = genfromtxt(carpeta+archivo_prefijo+str(i)+".dat")
        tensor.append(x)
        
    x = mean(tensor,axis=0)
    desvest = std(tensor,axis=0, ddof=1)
    return x,desvest