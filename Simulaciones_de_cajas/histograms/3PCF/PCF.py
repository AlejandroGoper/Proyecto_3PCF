#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 14:24:26 2021

@author: alejandro_goper

Clase para propagacion de errores de la 3PCF isotropica

Szapudi & Szalay - Estimator
"""

from numpy import ones,sqrt,genfromtxt,mean,std

class PCF:
    # Metodo constructor
    def __init__(self,_DDD,_DDR,_DRR,_RRR):
        # Atributos de clase
        self.DDD = _DDD
        self.DDR = _DDR
        self.DRR = _DRR
        self.RRR = _RRR
        
    """
        Se utiliza el estimador de Szapudi & Szalay
    """
    def estimar_3PCF(self):
        #Creamos un arreglo de unos de las mismas dimensiones que los histogramas
        one = ones((30,30,30))
        #Construimos el estimador
        est = self.DDD/self.RRR -3*self.DDR/self.RRR +3*self.DRR/self.RRR - one
        return est
    
    """
        Propagacion del error 
        
        Se toma como x -> DDD ; y -> DDR ; z -> DRR ; t -> RRR
    """
    def error_estimador_ss(self, e_DDD, e_DDR, e_DRR, e_RRR):
        error2 = (self.partial_x()*e_DDD)**2 + (self.partial_y()*e_DDR)**2 + (self.partial_z()*e_DRR)**2 + (self.partial_t()*e_RRR)**2
        error = sqrt(error2)
        return error
    
    
    """
        Derivadas parciales para la propagacion del error
    """
    
    def partial_x(self):
        return ones((30,30,30))/self.RRR        # 1/t
    
    def partial_y(self):
        return -3*self.partial_x()              # -3/t 
    
    def partial_z(self):
        return -self.partial_y()                # 3/t
    
    def partial_t(self):                        # -x/t2 + 3y/t2 - 3z/t2
        one_over_t = self.partial_x()
        one_over_t2 = one_over_t*one_over_t     
        return -self.DDD*one_over_t2 +3*self.DDR*one_over_t2-3*self.DRR*one_over_t2


"""
    Este modulo sirve para abrir los n archivos de alguno de los histogramas de determinada caja
    entrega un histograma resultado de haber promediado todas las realizaciones y entrega tambien
    la desviacion estandar de los valores del histograma como usarse como error
"""
def get_histogram(name,box,n_files):
    tensor = []
    if(name == "DDD"):
        carpeta = name+"/"
        archivo_prefijo = name+"iso_data_" + box + "_"
    elif(name == "DDR" or name == "DRR" or name =="RRR"):
        carpeta = name+"/"
        archivo_prefijo = name+"iso_rand0_" + box + "_"

    for i in range(n_files):
        # En este caso el archivo original esta guardado en 2D con dimensiones 900 x 30 
        x_2d = genfromtxt(carpeta+archivo_prefijo+str(i)+".dat")
        # Cambiamos de nuevo a histograma 3D
        x = x_2d.reshaped(30,30,30)
        tensor.append(x)
    # Promediamos todas las realizaciones
    x = mean(tensor,axis=0)
    # Realizamos la desviación estandar de todas las realizaciones
    desvest = std(tensor,axis=0, ddof=1)
    return x,desvest