from __future__ import division
import numpy as np
import os

os.chdir('/home/labosat/Desktop/Finazzi-Ferreira/Labo7/Vbr en T/vbrpython')

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


def weightedErrorR(measurements, weights):
    wTotal = 0
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    Rmean = weightedMean(measurements, weights)
    I = 0.0001
    V = I*Rmean
    V_err = V*0.00015 + 0.000225
    I_err = I*0.0003 + 0.00000006
    return np.sqrt(1/wTotal**2 + ((1/I)**2 * V_err**2 + (V/(I**2))**2 * I_err**2))

def weightedError(measurements, weights):
    wTotal = 0
    weights = np.asarray(weights)
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    mean = weightedMean(measurements, weights)
    rangeI = DetermineRange(0, mean)[1]
    error = MeasureError([mean], 'I', rangeI)
    return np.sqrt(1/wTotal**2 + (error[0])**2)


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

def exp(M, x):
    a, b, c = M
    return a * x**2 + b * x + c  

def exp_inv(M, x):
    a, b, c = M
    return 1/(a + b * np.exp(c * x))


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

def DerivateData(V, V_err, I, I_err):
    V_temp = []
    I_temp = []
    V_err_temp = []
    I_err_temp = []
    step = V[2] - V[1]
    for i in range(len(I)-1):
        I_temp.append((I[i + 1] - I[i - 1])/(2*step))
        V_temp.append(V[i])
        I_err_temp.append(((I_err[i + 1] - I_err[i - 1])/(2*step))**2)
        V_err_temp.append(V_err[i])
#    I_temp.remove(I[len(I)-1])   
#    I_temp.remove(I[len(I)-1])
#    V_temp.remove(V[len(V)-1])
#    V_temp.remove(V[len(V)-1])
#    I_err_temp.remove(I[len(I_err)-1])
#    I_err_temp.remove(I[len(I_err)-1])
#    I.remove(I[len(I)-1])
#    I.remove(I[len(I)-1])
    return V_temp, V_err_temp, I_temp, I_err_temp

def Smooth(V, V_err, I, I_err, degree):
    V_temp = []
    I_temp = []
    V_err_temp = []
    I_err_temp = []
    threshold = 0
    for i in range(len(I)-1):
        if abs(I[i+1]-I[i])> threshold:
            threshold = I[i]            
    for i in range(len(I)-1):
        if not abs(I[i + 1] - I[i]) > (threshold/2) or abs(I[i] - I[i - 1]) > (threshold / 2):
            V_temp.append(V[i])
            I_temp.append(I[i])
            V_err_temp.append(V_err[i])
            I_err_temp.append(I_err[i])
    return V, V_err, I, I_err



def error_I(I, source = False):
    temp = []
    percentage = 0
    offset = 0
    if source == True:
        for i in range(0, len(I)):
            if I[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I[i] and I[i] < 1*pow(10, -6):
                percentage = 0.0003
                offset = 800*pow(10, -12)    
            elif 1*pow(10, -6)<I[i] and I[i]<10*pow(10, -6): 
                percentage = 0.0003
                offset = 5*pow(10, -9)
            elif 10*pow(10, -6)<I[i] and I[i]<100*pow(10, -6): 
                percentage = 0.0003
                offset = 60*pow(10, -9)
            elif 100*pow(10, -6)<I[i] and I[i]<1*pow(10, -3): 
                percentage = 0.0003
                offset = 300*pow(10, -9)
            elif 1*pow(10, -3)<I[i] and I[i]<10*pow(10, -3): 
                percentage = 0.0003
                offset = 6*pow(10, -6)
            elif 10*pow(10, -3)<I[i] and I[i]<100*pow(10, -3): 
                percentage = 0.0003
                offset = 30*pow(10, -6)                
            elif 10*pow(10, -3)<I[i] and I[i]<1: 
                percentage = 0.0005
                offset = 1.8*pow(10, -3)
            elif 1<I[i] and I[i] < 1.5: 
                percentage = 0.0006
                offset = 4*pow(10, -3)
            else:
                percentage = 0.005
                offset = 40*pow(10, -3)
            temp.append(I[i]*percentage + offset)
            
    elif source==False:
        for i in range(0, len(I)):
            if I[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I[i] and I[i] < 1*pow(10, -6):
                percentage = 0.00025
                offset = 500*pow(10, -12)    
            elif 1*pow(10, -6)<I[i] and I[i]<10*pow(10, -6): 
                percentage = 0.00025
                offset = 1.5*pow(10, -9)
            elif 10*pow(10, -6)<I[i] and I[i]<100*pow(10, -6): 
                percentage = 0.0002
                offset = 25*pow(10, -9)
            elif 100*pow(10, -6)<I[i] and I[i]<1*pow(10, -3): 
                percentage = 0.0002
                offset = 200*pow(10, -9)
            elif 1*pow(10, -3)<I[i] and I[i]<10*pow(10, -3): 
                percentage = 0.0002
                offset = 2.5*pow(10, -6)
            elif 10*pow(10, -3)<I[i] and I[i]<100*pow(10, -3): 
                percentage = 0.0002
                offset = 20*pow(10, -6)                
            elif 10*pow(10, -3)<I[i] and I[i]<1: 
                percentage = 0.0003
                offset = 1.5*pow(10, -3)
            elif 1<I[i] and I[i] < 1.5: 
                percentage = 0.0005
                offset = 3.5*pow(10, -3)
            else:
                percentage = 0.004
                offset = 25*pow(10, -3)
            temp.append(I[i]*percentage + offset)
    else:
        print('Boolean values True or False.')
    return temp


def error_V(V, source = True):
    temp = []
    percentage = 0
    offset = 0
    if source == True:
        for i in range(0, len(V)):
            if V[i] < 200*pow(10, -3):
                percentage = 0.0002
                offset = 375*pow(10, -6)
            elif 200*pow(10, -3) < I[i] and I[i] < 2:
                percentage = 0.0002
                offset = 600*pow(10, -6)    
            elif 2<I[i] and I[i]<20: 
                percentage = 0.0002
                offset = 5*pow(10, -3)
            else:
                percentage = 0.002
                offset = 50*pow(10, -3)
            temp.append(I[i]*percentage + offset)
            
    elif source==False:
        for i in range(0, len(I)):
            if I[i] < 200*pow(10, -3):
                percentage = 0.00015
                offset = 225*pow(10, -6)
            elif 200*pow(10, -9) < I[i] and I[i] < 2:
                percentage = 0.0002
                offset = 350*pow(10, -6)    
            elif 2<I[i] and I[i]<20: 
                percentage = 0.00015
                offset = 5*pow(10, -3)
            else:
                percentage = 0.00015
                offset = 50*pow(10, -3)
            temp.append(I[i]*percentage + offset)
    else:
        print('Boolean values True or False.')
    return temp    
#Determines range of measurements automatically

def vbr(M, x):
    a, b = M
    return a/(x-b)
