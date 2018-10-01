from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from Funciones import Linear

data = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones_temporarias/Vbr/Estacionario 2/iv/17 (iv).txt')
V = data[1:, 0]
I = data[1:, 1] 
V_err = f.error_V(V)
I_err = f.error_I(I)

m, b, m_err, b_err, ks_stat, index = f.ks_iterative(V, I, V_err, I_err)

sigma = f.dispersion(I[1:len(V)-index])

k = 0
for i in range(len(V[1:])):
    if abs(I[i]) > abs((m*V[i] + b) + 2*sigma):
        print V[i]
        k = i
        break
print 'El voltaje de ruptura es %sV aprox.' % V[k] 

plt.plot(V, I, '.')
plt.errorbar(V, I, yerr=I_err, xerr=V_err, fmt='none')
plt.plot(V, V*m+b, lw = 3)
plt.plot(V[k], I[k], 'o')

plt.plot(V, np.cumsum(I), '.')

V_temp, V_err_temp, I_temp, I_err_temp = f.DerivateData(V, V_err, np.cumsum(I), np.cumsum(I_err))
m, b, m_err, b_err, ks_stat, index = f.ks_iterative(V_temp[1:], I_temp[1:], V_err_temp[1:], I_err_temp[1:])
plt.plot(V_temp[1:], I_temp[1:], '.')
plt.errorbar(V_temp[1:], I_temp[1:], yerr=I_err_temp[1:], xerr=V_err_temp[1:], fmt='none')

#%%
def Vbr_finder(path, tolerancia):
    """
    Calcula la resistencia de quenching y la temperatura (escrita en funcion de la
    resistencia que mide T) de un conjunto de mediciones, haciendo estadistica sobre los
    datos. 
    Es decir, si mido muchas curvas IV para una dada T, guardo las mediciones en una carpeta
    que contenga: una carpeta '/iv/' que contenga las curvas '/i (iv).txt' y otra carpeta
    '/res/' que contenga las resistencias '/i (res).txt'.
    Esta funcion va a calcular la Rq y la T para cada par (iv, res), y luego va a realizar
    un promedio pesado sobre las Rq y las T, devolviendo dichos parametros con sus errores.
    La funcion se va a encargar de filtrar aquellas mediciones en que la temperatura
    fluctuo mas que la tolerancia deseada, utilizando al funcion pulidor(). La tolerancia
    tipica es de 0.025 para mediciones estacionarias en T.
    El path de la funcion debe ser la carpeta donde se encuentren las carpetas iv y res.

    La funcion asume que la temperatura se midio con una RTD, sourceando corriente y
    midiendo voltaje.
    
    Input:  (path, tolerancia)   [string, float]    
    
    Returns: (R, R_err, Rq, Rq_err, chi2_out, array)  [float, float, float, float, float, list]
    .
    .
    """
    array = f.pulidor(tolerancia, path)
    R = []
    R_err = []
    Vbr = []
    Vbr_err = []
    for i in array:
        data1 = np.loadtxt(path+'/res/%s (res).txt' % i, skiprows=1)
        Res = data1[:, 1]   
        I = data1[:, 2]
        V = I*Res
        V_err = f.error_V(V, source = False)
        I_err = f.error_I(I, source = True)
        Res_err_estadistico = f.dispersion(Res) 
        Res_err_sistematico = [np.sqrt((1/I[j]**2) * V_err[j]**2 + ((V[j]/(I[j]**2))**2)*I_err[j]**2) for j in range(len(V))]
        Res_err = [np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico[j]**2) for j in range(len(V))]
        R.append(np.mean(Res))
        R_err.append(np.mean(Res_err))
        data2 = np.loadtxt(path+'/iv/%s (iv).txt' % i)
        V = data2[:, 0]
        I = data2[:, 1]
        I_err = f.error_I(I)
        V_err = f.error_V(V)
        m, b, m_err, b_err, ks_stat, index = f.ks_iterative(V, I, V_err, I_err)
        sigma = f.dispersion(I[1:len(V)-index])
        k = 0
        for i in range(len(V[1:])):
            if abs(I[i]) > abs((m*V[i] + b) + 2*sigma):
                k = i
                break
        Vbr.append(V[k])
        Vbr_err.append(V[2]-V[1])
    return R, R_err, Vbr, Vbr_err

path_grupos = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones_temporarias/Vbr'
Vbr_final = []
R_final = []
R_err_final = []
Vbr_err_final = []
for i in np.arange(0, 20):
    R, R_err, Vbr, Vbr_err = Vbr_finder(path_grupos + '/Estacionario %s' % i, 0.02 )
    Vbr_final.append(np.mean(Vbr))
    R_final.append(np.mean(R))
    R_err_final.append(np.mean(R_err))
    Vbr_err_final.append(np.mean(Vbr_err))
        
plt.plot(R_final, Vbr_final, '.')
plt.errorbar(R_final, Vbr_final, yerr=Vbr_err_final, xerr=R_err_final, fmt='none')
plt.xlabel('R (Ohms)')
plt.ylabel('Vbr (V)')


#%%        
def Vbr_finder(path, tolerancia):
    """
    Calcula la resistencia de quenching y la temperatura (escrita en funcion de la
    resistencia que mide T) de un conjunto de mediciones, haciendo estadistica sobre los
    datos. 
    Es decir, si mido muchas curvas IV para una dada T, guardo las mediciones en una carpeta
    que contenga: una carpeta '/iv/' que contenga las curvas '/i (iv).txt' y otra carpeta
    '/res/' que contenga las resistencias '/i (res).txt'.
    Esta funcion va a calcular la Rq y la T para cada par (iv, res), y luego va a realizar
    un promedio pesado sobre las Rq y las T, devolviendo dichos parametros con sus errores.
    La funcion se va a encargar de filtrar aquellas mediciones en que la temperatura
    fluctuo mas que la tolerancia deseada, utilizando al funcion pulidor(). La tolerancia
    tipica es de 0.025 para mediciones estacionarias en T.
    El path de la funcion debe ser la carpeta donde se encuentren las carpetas iv y res.

    La funcion asume que la temperatura se midio con una RTD, sourceando corriente y
    midiendo voltaje.
    
    Input:  (path, tolerancia)   [string, float]    
    
    Returns: (R, R_err, Rq, Rq_err, chi2_out, array)  [float, float, float, float, float, list]
    .
    .
    """
    array = f.pulidor(tolerancia, path)
    R = []
    R_err = []
    Vbr = []
    Vbr_err = []
    for i in array:
        data1 = np.loadtxt(path+'/res/%s (res).txt' % i, skiprows=1)
        Res = data1[:, 1]   
        I = data1[:, 2]
        V = I*Res
        V_err = f.error_V(V, source = False)
        I_err = f.error_I(I, source = True)
        Res_err_estadistico = f.dispersion(Res) 
        Res_err_sistematico = [np.sqrt((1/I[j]**2) * V_err[j]**2 + ((V[j]/(I[j]**2))**2)*I_err[j]**2) for j in range(len(V))]
        Res_err = [np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico[j]**2) for j in range(len(V))]
        R.append(np.mean(Res))
        R_err.append(np.mean(Res_err))
        data2 = np.loadtxt(path+'/iv/%s (iv).txt' % i)
        V = data2[:, 0]
        I = data2[:, 1]
        dI = f.error_I(I)
        dV = f.error_V(V)
        V_temp, V_err_temp, I_temp, I_err_temp = f.DerivateData(V, dV, np.cumsum(I), np.cumsum(dI))
        m, b, m_err, b_err, ks_stat, index = f.ks_iterative(V_temp[1:], I_temp[1:], V_err_temp[1:], I_err_temp[1:])
        Vbr.append(V[len(V)-index])
        Vbr_err.append(np.sqrt(((V[len(V)-index]*(m + m_err) + (b + b_err))-I[len(V)-1])**2 + (V[2]-V[1])**2))
        
    return R, R_err, Vbr, Vbr_err
        
path_grupos = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones_temporarias/Vbr'
Vbr_final = []
R_final = []
R_err_final = []
Vbr_err_final = []
for i in np.arange(0, 20):
    R, R_err, Vbr, Vbr_err = Vbr_finder(path_grupos + '/Estacionario %s' % i, 0.02 )
    Vbr_final.append(np.mean(Vbr))
    R_final.append(np.mean(R))
    R_err_final.append(np.mean(R_err))
    Vbr_err_final.append(np.mean(Vbr_err))
        
plt.plot(R_final, Vbr_final, '.')
plt.errorbar(R_final, Vbr_final, yerr=Vbr_err_final, xerr=R_err_final, fmt='none')
plt.xlabel('R (Ohms)')
plt.ylabel('Vbr (V)')