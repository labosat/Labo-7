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

def SourceError(A, source, scale):
    percentage = 0
    offset = 0
    if source == 'I':
        if scale == "10uA":
            percentage = 0.00033;
            offset = 2*pow(10, -9);
        elif scale == "100uA":
            percentage = 0.00031;
            offset = 20*pow(10, -9);
        else:
            print(scale + " is not a valid range.") 
        
    elif source == 'V':
        if scale == "2V":
            percentage = 0.0002;
            offset = 600*pow(10, -6);
        elif scale == "20V":
            percentage = 0.0002;
            offset = 2.4*pow(10, -3);
        elif scale == "200V":
            percentage = 0.0002;
            offset = 50*pow(10, -3);
        else:
            print(scale + " is not a valid range.") 
            
    else:
	    print("Source specified not understood") 
        
    temp = []
    for i in range(len(A)):
        result = A[i]*percentage + offset
        temp.append(result)
    return temp




def MeasureError(A, measure, scale):
    percentage = 0
    offset = 0
    if measure == 'I':
        if scale == "100nA":
            percentage = 0.0006
            offset = pow(100, -12)
        elif scale == '1uA':
            percentage = 0.00025
            offset = pow(500, -12)    
        elif scale == '10uA':
            percentage = 0.00025
            offset = 1.5*pow(10, -9)
        elif scale == '100uA':
            percentage = 0.00025
            offset = 6*pow(10,-9)
        elif scale == '10mA':
            percentage = 0.00035
            offset = 600*pow(10,-9)
        elif scale == '100mA':
            percentage = 0.00055
            offset = 6*pow(10, -6)
        else:
            print(str(scale) + ' is not a valid range.')
    elif measure == 'V':
        if scale == '2V':
            percentage = 0.00012
            offset = 300*pow(10, -6)
        elif scale == '20V':
            percentage = 0.00015
            offset = 1.5*pow(10,-3)
        elif scale == '200V':
            percentage = 0.0002
            offset = 24*pow(10,-3)
        else:
            print(str(scale) + ' is not a valid range.')
    else:
        print('Measure specified not understood.')
    
    temp = []
    for i in range(0, len(A)):
        temp.append(A[i]*percentage + offset)
    
    return temp

def MultiRange(I):
    temp = []
    percentage = 0
    offset = 0
    
    for i in range(0, len(I)):
        if I[i] < 10E-7:
            percentage = 0.0006
            offset = pow(100, -12)
        elif I[i] > 10E-7 and I[i] < 10E-6:
            percentage = 0.00025
            offset = pow(500, -12)    
        else: 
            percentage = 0.00025
            offset = 1.5*pow(10, -9)
            
        temp.append(I[i]*percentage + offset)
    return temp

#Determines range of measurements automatically
def DetermineRange(v, s):
    ranges_v = []
    ranges_i = []
	#in V
    range_lib_v = [0.2, 2., 20., 200.]
	#in I
    range_lib_i = [10**(-7), 10**(-6),  10**(-5), 10**(-4), 0.01, 0.1]
	
    for i in range(len(v)):
        range_v = 0
        range_i = 0
        number_v = 1
        number_i = 1
        output_range_v = 0
        output_range_i = 0
    
        comparison_v = [(abs(v[i] - range_lib_v[i])/range_lib_v[i]) for i in range(len(range_lib_v))]
        
        
        output_range_v = range_lib_v[comparison_v.index(np.min(comparison_v))]

        comparison_i = [(abs(s[i] - range_lib_i[i])/range_lib_i[i]) for i in range(len(range_lib_i))]
        output_range_i = range_lib_i[comparison_i.index(np.min(comparison_i))]
    
        if (output_range_v == 0.2):
            range_v = "200mV"
        elif (output_range_v == 2):
            range_v = "2V"
        elif (output_range_v == 20):
            range_v = "20V"
        elif output_range_v == 200:
            range_v = "200V"
    	
        if output_range_i == 10**(-7):
            range_i = "100nA"
        elif output_range_i == 10**(-6):
            range_i = "1uA"
        elif output_range_i == 10**(-5):
            range_i = "10uA"
        elif (output_range_i == 10**(-4)):
            range_i = "100uA"
        elif (output_range_i == 0.01):
            range_i = "10mA"
        elif (output_range_i == 0.1):
            range_i = "100mA"
    
        ranges_v.append(range_v)
        ranges_i.append(range_i)

    return ranges_v, ranges_i


def vbr(M, x):
    a, b = M
    return a/(x-b)
