import numpy as np
import matplotlib.pyplot as plt
from __future__ import division
import Funciones as f
from scipy.optimize import curve_fit
from scipy.odr import Model, RealData, ODR


#%%
def arrays(path, tolerancia):
    array = f.pulidor(tolerancia, path)
    R = []
    R_err = []
    for j in array:
        data1 = np.loadtxt(path+'/res/%s (res).txt' % j, skiprows=1)
        Res = data1[:, 1]   
        I = data1[:, 2]
        V = I*Res
        V_err = f.error_V(V, source = False)
        I_err = f.error_I(I, source = True)
        Res_err_estadistico = f.dispersion(Res) 
        Res_err_sistematico = [np.sqrt((1/I[i]**2) * V_err[i]**2 + ((V[i]/(I[i]**2))**2)*I_err[i]**2) for i in range(len(I))]
        Res_err = [np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico[i]**2) for i in range(len(Res_err_sistematico))]
        R.append(f.weightedMean(Res, Res_err))
        R_err.append(f.weightedError(Res, Res_err))
    return R, R_err, array
        
path_grupos = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Vbr/Mediciones LED prendido'
num_mediciones = 11
R_final = []
R_err_final = []
for i in np.arange(1, num_mediciones+1):
    R_temp, R_err_temp, array = arrays(path_grupos + '/Estacionario %s' % i, 0.025)
    R_final.append(f.weightedMean(R_temp, R_err_temp))
    R_err_final.append(f.weightedError(R_temp, R_err_temp))
    np.savetxt('array %s.txt' % i, array)
    
np.savetxt('R.txt', R_final)
np.savetxt('Rerr.txt', R_err_final)
#%%

data = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/12 (iv).txt')
I = data[:, 1]
V = data[:, 0]
I_err = f.error_I(I)
V_err = f.error_V(V)

I_log_err = [I_err[i]/I[i] for i in range(len(I))]

I_log = [np.log(i) for i in I]
V_temp, V_err_temp, I_temp, I_err_temp = f.DerivateData(V, V_err, I_log, I_log_err)

plt.plot(V_temp, I_temp, '.')
plt.errorbar(V_temp, I_temp, xerr=V_err_temp, yerr=I_err_temp, fmt='none')