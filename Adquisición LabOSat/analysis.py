#%% rq analysis

import numpy as np
from functions import tolerance, dispersion, weightedMean, error_R, error_V, error_I, Linear, ClosestToOne
from scipy.odr import ODR, Model, RealData

#def tolerance(tolerancia, path):
#    """
#    Esta funcion itera sobre todos los sets de datos que se encuentren en la carpeta 
#    del path, y filtra las N mediciones para quedarme solo con las que tienen
#    dispersion <= tolerancia. Me devuelve un array sobre el cual tengo analizar los datos,
#    asegurandome de que la dispersion en temperatura fue menor a la deseada.
#    No hay que poner el numero de mediciones, python las cuenta solo. 
#    Solo hay que poner el path!
#    Los archivos a iterar deben estar en una location terminada en '/res/i (res).txt', 
#    donde i es el numero de set de datos (de 1 a N).
#    Tolerancia tipica para mediciones en temperatura en el estacionario ==> 0.03
#    
#    Input: (tolerancia, path)
#    
#    Returns: list
#    .
#    .
#    """
#    filtro = []
#    i = 0
#    while True:
#        try:
#            i = i+1
#            data = np.loadtxt(path + '/%s.txt' % i, skiprows=1)
#            Res = data[:, 2]
#            if dispersion(Res) <= tolerancia:
#                filtro.append(i)
#        except IOError:
#            break
#        
#    return filtro


pixels = 18980
m = 3.81
#tolerance in temperature
tol = 0.1


folders = 15
R0 = 1000
Rq = []
T = []
Rq_err = []
T_err = []    

for i in range(1, folders + 1):

    #path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Adquisición LabOSat/results/Encapsulado 1/%s (rq)' % i
    path = 'C:/Users/lucas/Documents/GitHub/Labo-7/Adquisición LabOSat/results/Encapsulado 1 con grasa/%s (rq)' % i

    Rq_temp = []
    T_temp = []
    Rq_err_temp = []
    T_err_temp = []
    #casa
    array = tolerance(tol, path)
    end = len(array)
    

    for j in array:
    #path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s' % i
        
        path_group = '/%s.txt' % j
        data_vbr = np.loadtxt(path + path_group, skiprows=1)
        V = data_vbr[:, 0]
        I = data_vbr[:, 1]
        R = data_vbr[:, 2]
        V_err = error_V(V, '2612')
        I_err = error_I(I, '2612')
            
        chi_2 = []
        beta = []
        sd_beta = []
        t = (np.mean(R) - R0)/m
        t_err = np.sqrt((np.std(R)/m)**2 * 1/len(R) + 1/m**2)
        
        for h in range(len(V) - 2):
            V_fit = V[h:]
            I_fit = I[h:]
            I_err_fit = I_err[h:]
            V_err_fit = V_err[h:]
            model = Model(Linear)
            data = RealData(V_fit, I_fit, sx=V_err_fit, sy=I_err_fit)
            odr = ODR(data, model, beta0=[0., 0.], maxit=1000000)
            out = odr.run()
            
            beta.append(out.beta[0])
            sd_beta.append(out.sd_beta[0])
            chi_2.append(out.res_var)


      
        index = ClosestToOne(chi_2)
        Rq_temp.append(pixels/beta[index])
        Rq_err_temp.append(pixels/(beta[index]**2)*sd_beta[index])
        T_temp.append(t)
        T_err_temp.append(t_err)
        print("%s/%s" % (j, end))
        
    Rq.append(np.mean(Rq_temp))
    T.append(np.mean(T_temp))
    Rq_err.append(np.mean(Rq_err_temp))
    T_err.append(np.mean(T_err_temp))
    print("success!: "+ str(i))
        
import matplotlib.pyplot as plt
plt.errorbar(T, Rq, xerr=T_err, yerr=Rq_err, fmt='.k', capsize=3)
    
#%% vbr analysis
    
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData
import time

def LogData(x, y, y_err):
    v = [np.log(a) for a in y]
    v_err = []
    for i in range(0, len(y)):
        v_err.append(y_err[i]/y[i])
    return x, v, v_err

def DiffData(x, y, x_err, y_err):
    h = x[1] - x[0]
    diff = []
    diff_err = []
    for i in range(1, len(y) - 1):
        diff.append((y[i - 1] - y[i + 1])/(2*h))
        diff_err.append(np.sqrt((abs(y_err[i - 1])**2 + abs(y_err[i + 1])**2))/(2*h))
        
    index = [0, len(x) - 1]    
        
    x = np.delete(x, index)
    x_err = np.delete(x_err, index)
    
    return x, diff, x_err, diff_err


def dispersion(x):
    """
    Esta funcion calcula la standard deviation de una muestra 'x'.
    
    Input: x  (list or array)
    
    Returns: int
    .
    .
    """
    return np.sqrt(np.sum(((x - np.mean(x))**2)/(len(x)-1)))

def error_I(y, SMU, source = False):
    """
    Esta funcion esta diseniada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonc
    I_led_temp_1 = I_led[1:int(len(I_led)/2)]es la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    if SMU == '2612':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.0003
                    offset = 800*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.0003
                    offset = 5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0003
                    offset = 60*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0003
                    offset = 300*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0003
                    offset = 6*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0003
                    offset = 30*pow(10, -6)                
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0005
                    offset = 1.8*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <= 1.5: 
                    percentage = 0.0006
                    offset = 4*pow(10, -3)
                else:
                    percentage = 0.005
                    offset = 40*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00025
                    offset = 500*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.00025
                    offset = 1.5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0002
                    offset = 25*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0002
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0002
                    offset = 2.5*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0002
                    offset = 20*pow(10, -6)                
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0003
                    offset = 1.5*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <=1.5: 
                    percentage = 0.0005
                    offset = 3.5*pow(10, -3)
                else:
                    percentage = 0.004
                    offset = 25*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00029
                    offset = 300*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00027
                    offset = 700*pow(10, -12)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00025
                    offset = 6*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00027
                    offset = 60*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00035
                    offset = 600*pow(10, -9)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00055
                    offset = 6*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0022
                    offset = 570*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00035
                    offset = 600*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00033
                    offset = 2*pow(10, -9)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00031
                    offset = 20*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00034
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00045
                    offset = 2*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00066
                    offset = 20*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0027
                    offset = 900*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')        
    
    return temp


def error_V(x, SMU, source = True):
    """
    Esta funcion esta diseniada para crear un array con los errores del voltaje 
    medido o sourceado por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene el voltaje, y un boolean que indica si el 
    mismo fue medido o sourceado.
    
    Input: (V, source = True)
    
    Si no se especifica el source, entonces el voltaje fue sourceado. Si source = False,
    entonces se midio voltaje.
    
    Returns:  V_err  (list)
    .
    .
    """
    if SMU == '2612':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 375*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00015
                    offset = 225*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 350*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 600*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 2.4*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 24*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00012
                    offset = 300*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.00012
                    offset = 300*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 1.5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 10*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
        
    return temp    

def pulidor(tolerancia, path):
    """
    Esta funcion itera sobre todos los sets de datos que se encuentren en la carpeta 
    del path, y filtra las N mediciones para quedarme solo con las que tienen
    dispersion <= tolerancia. Me devuelve un array sobre el cual tengo analizar los datos,
    asegurandome de que la dispersion en temperatura fue menor a la deseada.
    No hay que poner el numero de mediciones, python las cuenta solo. 
    Solo hay que poner el path!
    Los archivos a iterar deben estar en una location terminada en '/res/i (res).txt', 
    donde i es el numero de set de datos (de 1 a N).
    Tolerancia tipica para mediciones en temperatura en el estacionario ==> 0.03
    
    Input: (tolerancia, path)
    
    Returns: list
    .
    .
    """
    filtro = []
    i = 0
    while True:
        try:
            i = i+1
            data = np.loadtxt(path + '/%s.txt' % i, skiprows=1)
            Res = data[:, 2]
            if dispersion(Res) <= tolerancia:
                filtro.append(i)
        except IOError:
            break
        
    return filtro

def ClosestToOne(v):
    """
    Esta funcion toma una lista, y devuelve el indice del elemento mas cercano a 1 de 
    la lista.
    
    Input: list
    
    Returns: int  (index)
    .
    .
    """
    compliance = []
    compliance_not_1 = []
    for j in range(0, len(v)):
        compliance.append(abs(v[j] - 1))
    for j in compliance:
        if j != 1:
            compliance_not_1.append(j)
    return compliance_not_1.index(np.min(compliance_not_1))


def fit_function(M, x):
    a, b = M
    return a/(x - b)


def fit_calc(beta, sd_beta, value, perfect = False):
    temp = []
    temp2 = []
    temp3 = []
    for i in range(0, len(beta)):
        if perfect:
            temp.append(beta[i][0])
            temp2.append(beta[i][1])
            temp3.append(sd_beta[i][1])
        else:
            if beta[i][0] != value:
                temp.append(beta[i][0])
                temp2.append(beta[i][1])
                temp3.append(sd_beta[i][1])
    for i in range(0, len(temp)):
        if perfect:
            if temp[i] == value:
                return value
            
        else:
            temp = [x/value for x in temp]
            i = ClosestToOne(temp)
            beta_temp = [beta[i][0] for i in range(len(beta))]
            j = beta_temp.index(value * temp[i])
            return j, temp2[i], temp3[i]


def weightedMean(measurements, weights):
    """
    Devuelve el promedio pesado de una muestra con sus respectivos errores.
    
    Input: (X, X_err)  lists
    
    Returns: float
    .
    .
    """
    wTotal = np.sum([1/i**2 for i in weights])
    mwTotal = 0
    mean = 0 
#    for i in range(0, len(weights)):
#        wTotal += (1 / weights[i]**2)
    for i in range(0, len(measurements)):
        mwTotal += measurements[i]*(1/weights[i]**2)
    mean = mwTotal / wTotal 
    return mean

def weightedError(measurements, weights):
    """
    A chequear
    """
    wTotal = 0
    weights = np.asarray(weights)
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    return np.sqrt(1/wTotal)

def QuadSum(v):
    result = 0
    for i in range(len(v)):
        result += v[i]*v[i]
        
    return np.sqrt(result/len(v))

m = 3.81
R0 = 1000
max_limit = 25
folders = 3
tolerancia = 1
#j = 5

start = time.time()
T = []
T_err = []
Vbr = []
Vbr_err = []
p0 = []
p0_err = []
T_lista = []
T_err_lista = []
Vbr_lista = []
Vbr_err_lista = []



for i in range(1, folders + 1):

    path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Adquisición LabOSat/results/Encapsulado 1 con grasa/%s (vbr)' % i
    Vbr_temp = []
    T_temp = []
    Vbr_err_temp = []
    T_err_temp = []

    array = pulidor(tolerancia, path)
    end = len(array)
    

    for j in array:        
        path_group = '/%s.txt' % j
        data_vbr = np.loadtxt(path + path_group, skiprows=1)
        V = data_vbr[:, 0]
        I = data_vbr[:, 1]
        R = data_vbr[:, 2]
        V_err = error_V(V, '2612')
        I_err = error_I(I, '2612')
    
    
        V, I, I_err = LogData(V, I, I_err)
        V, I, V_err, I_err = DiffData(V, I, V_err, I_err)

#        Para chequear con los dedos.
#        plt.plot(V, I, '.')
#        asd = [23.9, 24.12, 24.04, 23.8]
#        asd_T = [881.7, 926.4, 900.5, 855.9]

        #flag to check if data needs to be inverted
        I = I[1:]
        V = V[1:]
        I_err = I_err[1:]
        V_err = V_err[1:]
        
        if abs(np.max(I)) > abs(np.min(I)):
            index = I.index(np.max(I)) + 1
        elif abs(np.max(I)) < abs(np.min(I)):
            index = I.index(np.min(I)) + 1
            I = [-x for x in I]
            
        chi_2 = []
        beta = []
        beta2 = []
        sd_beta = []
        t = (np.mean(R) - R0)/m
        t_err = np.sqrt((np.std(R)/m)**2 * 1/len(R) + 1/m**2)
        
        for l in range(1, 2):
            for h in range(l + 1, len(V[index:]) + max_limit):
                V_fit = V[index + l:index + h]
                I_fit = I[index + l:index + h]
                I_err_fit = I_err[index + l:index + h]
                V_err_fit = V_err[index + l:index + h]
                model = Model(fit_function)
                data = RealData(V_fit, I_fit, sx=V_err_fit, sy=I_err_fit)
                odr = ODR(data, model, beta0=[2, 27.], maxit=1000000)
                out = odr.run()
                
                #chi_2.append(dispersion(V_fit, I_fit, I_err_fit, out.beta))
                if not np.isnan(out.beta[0]):
                    beta.append(out.beta)
                    sd_beta.append(out.sd_beta)
                #print(h)

      
        index_chi, vbr, vbr_err = fit_calc(beta, sd_beta, 2)
        Vbr_temp.append(vbr)
        Vbr_err_temp.append(vbr_err)
        T_temp.append(t)
        T_err_temp.append(t_err)
        print("%s/%s" % (j, end))
        
        
    #aca estan los datos antes de promediar como lista de listas
    T_lista.append(T_temp)
    T_err_lista.append(T_err_temp)
    Vbr_lista.append(Vbr_temp)
    Vbr_err_lista.append(Vbr_err_temp)
    
    T.append(weightedMean(T_temp, T_err_temp))
    T_err.append(weightedError(T_temp, T_err_temp))
    Vbr.append(weightedMean(Vbr_temp, Vbr_err_temp))
    Vbr_err.append(weightedError(Vbr_temp, Vbr_err_temp))
    
#    plt.plot(V, I, '.')
#    plt.plot(V, fit_function(beta[index_chi], V))
    #p0.append(beta[])
    print("success!: "+ str(i))
    

print(str(time.time() - start) + " seconds")

plt.figure(1)
plt.errorbar(T, Vbr, xerr= T_err, yerr= Vbr_err, fmt='or', capsize= 3)
plt.grid(True)

linear_model = Model(Linear)
data = RealData(T, Vbr, sx=T_err, sy=Vbr_err)
odr = ODR(data, linear_model, beta0=[0., 1.])
out = odr.run()
    
m = out.beta[0]
b = out.beta[1]
m_err = out.sd_beta[0]
b_err = out.sd_beta[1]        
chi2 = out.res_var
plt.plot(T, [T[i]*m + b for i in range(len(T))])
plt.xlabel('Temperatura (C)')
plt.ylabel('Breakdown Voltage (V)')


R = T[0]*3.815 + 1000
dR = T_err[0]*3.815 + 2.6

print("9\t"+str(Vbr[0])+"\t"+str(Vbr_err[0]*np.sqrt(len(Vbr_err_temp)))+"\t"+str(Vbr_err[0])+"\t"+str(Vbr_err[0]/np.sqrt(len(Vbr_err_temp)))+"\t"+str(R)+"\t"+str(dR))


plt.figure(2)
for k in range(len(T_lista)):
    plt.errorbar(T_lista[k], Vbr_lista[k], xerr = T_err_lista[k], yerr = Vbr_err_lista[k], fmt = 'ob', capsize = 3)
plt.grid(True)
plt.xlabel('Temperatura (C)')
plt.ylabel('Breakdown Voltage (V)')



#%% i dark analysis

def error_I(y, SMU, source = False):
    """
    Esta funcion esta diseniada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonc
    I_led_temp_1 = I_led[1:int(len(I_led)/2)]es la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    if SMU == '2612':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.0003
                    offset = 800*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.0003
                    offset = 5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0003
                    offset = 60*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0003
                    offset = 300*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0003
                    offset = 6*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0003
                    offset = 30*pow(10, -6)                
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0005
                    offset = 1.8*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <= 1.5: 
                    percentage = 0.0006
                    offset = 4*pow(10, -3)
                else:
                    percentage = 0.005
                    offset = 40*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00025
                    offset = 500*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.00025
                    offset = 1.5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0002
                    offset = 25*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0002
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0002
                    offset = 2.5*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0002
                    offset = 20*pow(10, -6)                
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0003
                    offset = 1.5*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <=1.5: 
                    percentage = 0.0005
                    offset = 3.5*pow(10, -3)
                else:
                    percentage = 0.004
                    offset = 25*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00029
                    offset = 300*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00027
                    offset = 700*pow(10, -12)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00025
                    offset = 6*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00027
                    offset = 60*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00035
                    offset = 600*pow(10, -9)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00055
                    offset = 6*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0022
                    offset = 570*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00035
                    offset = 600*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00033
                    offset = 2*pow(10, -9)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00031
                    offset = 20*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00034
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00045
                    offset = 2*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00066
                    offset = 20*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0027
                    offset = 900*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')        
    
    return temp


def error_V(x, SMU, source = True):
    """
    Esta funcion esta diseniada para crear un array con los errores del voltaje 
    medido o sourceado por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene el voltaje, y un boolean que indica si el 
    mismo fue medido o sourceado.
    
    Input: (V, source = True)
    
    Si no se especifica el source, entonces el voltaje fue sourceado. Si source = False,
    entonces se midio voltaje.
    
    Returns:  V_err  (list)
    .
    .
    """
    if SMU == '2612':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 375*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00015
                    offset = 225*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 350*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 600*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 2.4*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 24*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00012
                    offset = 300*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.00012
                    offset = 300*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 1.5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 10*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
        
    return temp    

def error_R(v):
    r_temp = [i*0.0007 + 0.3 for i in v]
    return r_temp
        

def pulidor_dark(tolerancia, path):

    filtro = []
    i = 0
    while True:
        try:
            i = i+1
            data = np.loadtxt(path + '/%s.txt' % i, skiprows=1)
            Res = data[:, 1]
            if dispersion(Res) <= tolerancia:
                filtro.append(i)
        except IOError:
            break
        
    return filtro

m = 3.81
R0 = 1000
max_limit = 0
folders = 11
tolerancia = 0.1
I_dark = []
R_dark = []
I_dark_err = []
R_dark_err = []
for k in range(1, folders + 1):
    
    #path_dark = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Adquisición LabOSat/results/Encapsulado 1/%s (idark)' % k
    path_dark = 'C:/Users/lucas/Documents/GitHub/Labo-7/Adquisición LabOSat/results/Encapsulado 1 con grasa/%s (idark)' % k

    array = pulidor_dark(1, path_dark)
    end = len(array)
    I_dark_temp = []
    R_dark_temp = []
    I_dark_err_temp = []
    R_dark_err_temp = []

    for j in array:
        path_group = '/%s.txt' % j
        data_i_dark = np.loadtxt(path_dark + path_group, skiprows=1)
        I_dark_temp.append(data_i_dark[:, 0])
        R_dark_temp.append((data_i_dark[:, 1]))
        I_dark_err_temp.append(error_I(data_i_dark[:, 0], '2612'))
        R_dark_err_temp.append(error_R(data_i_dark[:, 1]))
        
    I_dark.append(np.mean(I_dark_temp))
    R_dark.append((np.mean(R_dark_temp) - 1000)/m)
    I_dark_err.append(np.mean(I_dark_err_temp))
    R_dark_err.append(np.mean(R_dark_err_temp)/m)


#plt.figure(3)
#for k in range(len(I_dark)):
#    plt.plot(R_dark[k], I_dark[k], '.')
plt.errorbar(R_dark, I_dark, xerr=R_dark_err, yerr=I_dark_err, fmt='.k', capsize=3)
plt.xlabel("Temperature [ºC]")
plt.ylabel("Dark Current [A]")
plt.grid(True)
plt.tight_layout(True)
    

