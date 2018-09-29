from __future__ import division
import numpy as np
import os

os.chdir('/home/labosat/Desktop/Finazzi-Ferreira/Labo7/Rq en T')

def weightedMean(measurements, weights):
    wTotal = 0
    mwTotal = 0
    mean = 0
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    for i in range(0, len(measurements)):
        mwTotal += measurements[i]*(1/weights[i]**2)
    mean = mwTotal / wTotal 
    return mean


def weightedError(measurements, weights):
    wTotal = 0
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    Rmean = weightedMean(measurements, weights)
    I = 0.0001
    V = I*Rmean
    V_err = V*0.0002 + 0.0006
    I_err = I*0.0003 + 0.00000006
    return np.sqrt(1/wTotal**2 + ((1/I)**2 * V_err**2 + (V/(I**2))**2 * I_err**2))

def dispersion(x):
    return np.sqrt(np.sum(((x - np.mean(x))**2)/(len(x)-1)))

def pulidor(tolerancia, path):
    filtro = []
    i = 0
    while True:
        try:
            i = i+1
            data = np.loadtxt(path + '/res/%s (res).txt' % i, skiprows=1)
            Res = data[:, 1]
            if dispersion(Res) <= tolerancia:
                filtro.append(i)
        except IOError:
            break
#Esta funcion filtra las N mediciones para quedarme solo con las que tienen
#tolerancia = tolerancia. Me devuelve el array sobre el cual tengo que iterar
#Para luego sacar la R y Rq.    No hay que poner el numero de mediciones, python
#las cuenta solo. Solo hay que poner el path!
#Tolerancia tipica para el estacionario ==> 0.03
    return filtro
# path = '/home/tomas/Desktop/Labo 6 y 7/Medicion Rq en T/k2612B/Mediciones estacionarias/Grupo 8'

def ClosestToOne(v):
    compliance = []
    for j in range(0, len(v)):
        compliance.append(abs(v[j] - 1))
    return compliance.index(np.min(compliance))

def Linear(M, x):
    m, b = M
    return m*x + b


def promediar_puntos(p, eje_y, eje_x):
    array_promediado = []
    array_tiempo_promediado = []
    array1 = eje_y
    array2 = eje_x
    for j in range(int(len(array1)/p)):
        total = 0   
        total_tiempo = 0
        for i in range(p):
            total += array1[j * p + i] / float(p)
            total_tiempo += array2[j * p + i] / float(p)
        array_promediado.append(total)
        array_tiempo_promediado.append(total_tiempo)
    return array_promediado, array_tiempo_promediado
