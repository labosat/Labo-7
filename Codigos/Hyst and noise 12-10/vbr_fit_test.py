#este script trata de encontrar vbr derivando un fit polinomico de grado 6
#resultados al final

import numpy as np
import matplotlib.pyplot as plt

def error_I(y, source = False):
    """
    Esta funcion esta diseñada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonces la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    I_temp= y
    temp = []
    percentage = 0
    offset = 0
    if source == True:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.0003
                offset = 800*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.0003
                offset = 5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0003
                offset = 60*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0003
                offset = 300*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0003
                offset = 6*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0003
                offset = 30*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0005
                offset = 1.8*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0006
                offset = 4*pow(10, -3)
            else:
                percentage = 0.005
                offset = 40*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
            
    elif source==False:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.00025
                offset = 500*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.00025
                offset = 1.5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0002
                offset = 25*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0002
                offset = 200*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0002
                offset = 2.5*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0002
                offset = 20*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0003
                offset = 1.5*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0005
                offset = 3.5*pow(10, -3)
            else:
                percentage = 0.004
                offset = 25*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
    else:
        print('Boolean values True or False.')
    return temp

def derive_poly(x, v):
    numerator = 0
    denominator = 0
    for i in range(0, len(v) - 1):
        numerator += (len(v) - 1 - i)*v[len(v) - 2 - i]*pow(x, len(v) - 1 - i)
        
    for i in range(0, len(v)):
        denominator += v[len(v) - 1 - i]*pow(x, i)
    
    return numerator/denominator

#select which temperature to load
i = 1

#casa
#path = '/home/lucas/Desktop/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s/iv/7 (iv).txt' % i

#labo windows
path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s/iv/7 (iv).txt' % i

data = np.loadtxt(path)

V = data[:, 0]
I = data[:, 1] 
I_err = error_I(I)

plt.errorbar(V, I, yerr=I_err, fmt='.')

fit = np.polyfit(V, I, 6)
plt.plot(V, derive_poly(V, fit), "r--", lw = 2)




T = []
for i in range(1, 14):
    #path = '/home/lucas/Desktop/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s/res/7 (res).txt' % i
    path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s/iv/7 (iv).txt' % i

    data = np.loadtxt(path, skiprows=1)
    t = 0
    R = data[:, 1]
    t = (np.mean(R) - 1000)/3.815
    T.append(t)
    
  
#grafico de lo conseguido    
#data_test = np.loadtxt('/home/lucas/Desktop/vbr.txt')
#T = data_test[:, 2]
#Vbr = data_test[:, 1]

#fit = np.polyfit(T, Vbr, 1)

#plt.plot(T, Vbr, '.')
#plt.plot(T, np.polyval(fit, T), "r--", lw = 2)
#plt.grid(True)
#plt.xlabel('Temperature [ºC]')
#plt.ylabel('Breakdown Voltage [V]')   

#%% automatization of peak finding method above
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def error_I(y, source = False):
    """
    Esta funcion esta diseñada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonces la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    I_temp= y
    temp = []
    percentage = 0
    offset = 0
    if source == True:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.0003
                offset = 800*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.0003
                offset = 5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0003
                offset = 60*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0003
                offset = 300*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0003
                offset = 6*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0003
                offset = 30*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0005
                offset = 1.8*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0006
                offset = 4*pow(10, -3)
            else:
                percentage = 0.005
                offset = 40*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
            
    elif source==False:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.00025
                offset = 500*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.00025
                offset = 1.5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0002
                offset = 25*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0002
                offset = 200*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0002
                offset = 2.5*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0002
                offset = 20*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0003
                offset = 1.5*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0005
                offset = 3.5*pow(10, -3)
            else:
                percentage = 0.004
                offset = 25*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
    else:
        print('Boolean values True or False.')
    return temp

def derive_poly(x, v):
    numerator = 0
    denominator = 0
    for i in range(0, len(v) - 1):
        numerator += (len(v) - 1 - i)*v[len(v) - 2 - i]*pow(x, len(v) - 1 - i)
        
    for i in range(0, len(v)):
        denominator += v[len(v) - 1 - i]*pow(x, i)
    
    return numerator/denominator

def Linear(M, x):
    """
    Funcion lineal para ajustar con el ODR:
        
    >>> linear_model = Model(Linear)
    >>> data = RealData(X, Y, sx=X_err, sy=Y_err)
    >>> odr = ODR(data, linear_model, beta0=[0., 1.])
    >>> out = odr.run()
    
    >>> m = out.beta[0]
    >>> b = out.beta[1]
    >>> m_err = out.sd_beta[0]
    >>> b_err = out.sd_beta[1]        
    >>> chi2 = out.res_var
    .
    .
    """
    m, b = M
    return m*x + b

def Find(v, x, tolerance = 0.01):
    for i in range(0, len(v)):
        if abs(v[i] - x) < tolerance:
            return i
    return 0

folders = 12
Vbr = []
T = []


for i in range(1, folders + 1):
    j = 1
    path = '/home/lucas/Desktop/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s' % i
    
    #labo windows
    #path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s' % i

    breakdown = 0
    temp = 0
    
    while True:
        try:
            path_group_i = '/iv/%s (iv).txt' % j
            path_group_r = '/res/%s (res).txt' % j
    
            data_i = np.loadtxt(path + path_group_i)
            data_r = np.loadtxt(path + path_group_r, skiprows=1)
            
            V = data_i[:, 0]
            I = data_i[:, 1]
            I_err = error_I(I)
            R = data_r[:, 1]
            
            fit = np.polyfit(V, I, 6, w=I_err)
            
            peaks = signal.find_peaks(derive_poly(V, fit), threshold=1000)
            max_index = np.max(peaks[0])
    
            breakdown += V[max_index]
            temp += (np.mean(R) - 1000)/3.815
        
            j += 1
        except IOError:
            break
    
    
    breakdown = breakdown/(j - 1)
    temp = temp/(j - 1)
    Vbr.append(breakdown)
    T.append(temp)

T_err = [0.655 for x in T]
#minimo step en la medicion - ver mejor este error
Vbr_err = [0.002*x for x in Vbr]

np.savetxt('/home/lucas/Desktop/data_vbr.txt', np.c_[T, Vbr])

plt.errorbar(T, Vbr, xerr=T_err, yerr=Vbr_err, fmt='.')
plt.grid(True)
plt.xlabel('Temperature [C]')
plt.ylabel('Breakdown Voltage [V]')


fit = np.polyfit(T, Vbr, 1, w=Vbr_err)
plt.plot(T, np.polyval(fit, T))
    
fit
    

vbr_lib = [0.0204502821*x + 24.2680092 for x in T]
    

folders = 12
Vbr = []
T = []


for i in range(1, folders + 1):
    j = 1
    path = '/home/lucas/Desktop/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s' % i
    
    #labo windows
    #path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s' % i

    breakdown = 0
    temp = 0
    
    while True:
        try:
            path_group_i = '/iv/%s (iv).txt' % j
            path_group_r = '/res/%s (res).txt' % j
    
            data_i = np.loadtxt(path + path_group_i)
            data_r = np.loadtxt(path + path_group_r, skiprows=1)
            
            V = data_i[Find(data_i[:, 0], vbr_lib[i - 1], 0.01) - 25:, 0]
            I = data_i[Find(data_i[:, 0], vbr_lib[i - 1], 0.01) - 25:, 1]
            I_err = error_I(I)
            R = data_r[:, 1]
            
            fit = np.polyfit(V, I, 6, w=I_err)
            
            if (abs(np.max(derive_poly(V, fit))) > abs(np.min(derive_poly(V, fit)))):
                max_index = np.where(derive_poly(V, fit) == np.max(derive_poly(V, fit)))[0][0]
            else:
                max_index = np.where(derive_poly(V, fit) == np.min(derive_poly(V, fit)))[0][0]
    
            breakdown += V[max_index]
            temp += (np.mean(R) - 1000)/3.815
        
            j += 1
        except IOError:
            break
    
    
    breakdown = breakdown/(j - 1)
    temp = temp/(j - 1)
    Vbr.append(breakdown)
    T.append(temp)

T_err = [0.655 for x in T]
#minimo step en la medicion - ver mejor este error
Vbr_err = [0.002*x for x in Vbr]

np.savetxt('/home/lucas/Desktop/data_vbr.txt', np.c_[T, Vbr])

plt.errorbar(T, Vbr, xerr=T_err, yerr=Vbr_err, fmt='.')
plt.grid(True)
plt.xlabel('Temperature [C]')
plt.ylabel('Breakdown Voltage [V]')


fit = np.polyfit(T, Vbr, 1, w=Vbr_err)
plt.plot(T, np.polyval(fit, T))
    
fit

#%% test to check labo6 method (without xerr for now)
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def LogData(x, y, y_err):
    v = [np.log(a) for a in y]
    v_err = []
    for i in range(0, len(y)):
        v_err.append(y_err[i]/y[i])
    return x, v, v_err

def DiffData(x, y, y_err):
    h= x[1] - x[0]
    diff = []
    diff_err = []
    for i in range(1, len(y) - 1):
        diff.append((y[i - 1] - y[i + 1])/(2*h))
        diff_err.append((abs(y_err[i - 1]) + abs(y_err[i + 1]))/(2*h))
        
    index = [0, len(x) - 1]    
        
    x = np.delete(x, index)
    
    return x, diff, diff_err

def error_I(y, source = False):
    """
    Esta funcion esta diseñada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonces la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    I_temp= y
    temp = []
    percentage = 0
    offset = 0
    if source == True:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.0003
                offset = 800*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.0003
                offset = 5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0003
                offset = 60*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0003
                offset = 300*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0003
                offset = 6*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0003
                offset = 30*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0005
                offset = 1.8*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0006
                offset = 4*pow(10, -3)
            else:
                percentage = 0.005
                offset = 40*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
            
    elif source==False:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.00025
                offset = 500*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.00025
                offset = 1.5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0002
                offset = 25*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0002
                offset = 200*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0002
                offset = 2.5*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0002
                offset = 20*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0003
                offset = 1.5*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0005
                offset = 3.5*pow(10, -3)
            else:
                percentage = 0.004
                offset = 25*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
    else:
        print('Boolean values True or False.')
    return temp

def fit_function(M, x):
    a, b = M
    return a/(x - b)

i = 2
j = 1

#casa
#path = '/home/lucas/Desktop/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s' % i

#labo windows
path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario %s' % i


path_group_i = '/iv/%s (iv).txt' % j
data_i = np.loadtxt(path + path_group_i, skiprows=1)
V = data_i[:, 0]
I = data_i[:, 1]
I_err = error_I(I)

V, I, I_err = LogData(V, I, I_err)
V, I, I_err = DiffData(V, I, I_err)

from scipy.odr import ODR, Model, RealData

#flag to check if data needs to be inverted
flag = False

if abs(np.max(I)) > abs(np.min(I)):
    maxim = np.max(I)
    for i in range(0, len(I)):
        if I[i] == maxim:
            index = i
elif abs(np.max(I)) < abs(np.min(I)):
    minim = np.min(I)
    for i in range(0, len(I)):
        if I[i] == minim:
            index = i
    I = [-x for x in I]

        
#plt.errorbar(V, I, yerr=I_err, fmt='.')

V_fit = []
I_fit = []
I_err_fit = []
for i in range(index + 1, index + 15):
    V_fit.append(V[i])
    I_fit.append(I[i])
    I_err_fit.append(I_err[i])
    
plt.errorbar(V_fit, I_fit, yerr=I_err_fit, fmt='.')

model = Model(fit_function)
data = RealData(V_fit, I_fit, sx=I_err_fit)
odr = ODR(data, model, beta0=[2., 25.], maxit=10000)
out = odr.run()

p0 = out.beta[0]
p1 = out.beta[1]

plt.plot(V_fit,  fit_function(out.beta, V_fit))
