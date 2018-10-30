from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData
import copy

def Exp(M, x):
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
    a, b, c = M
    return a*pow((x/300), b)*np.exp(-c/x)


data1 = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Graficos y txt/txts/data_rq_final.txt', skiprows=1)
T_celcius = (data1[:, 3] - 1000)/3.815
T = [T_celcius[i] + 273 for i in range(len(T_celcius))]
T_err = (data1[:, 4])/3.815
Rq = data1[:, 1]
Rq_err = data1[:, 2]

plt.figure(1)
plt.errorbar(T, Rq, xerr= T_err, yerr= Rq_err, fmt='k.', capsize= 3)
model = Model(Exp)
data = RealData(T, Rq, sx=T_err, sy=Rq_err)
odr = ODR(data, model, beta0=[400000., 1., -65], maxit=100000)
out = odr.run()
    
a = out.beta[0]
b = out.beta[1]
c = out.beta[2]
a_err = out.sd_beta[0]
b_err = out.sd_beta[1]        
c_err = out.sd_beta[2]
chi2 = out.res_var
T_2 = copy.deepcopy(T)
T_3 = np.linspace(min(T), max(T), 2000)
T_2.sort()
#plt.plot(T_2, Exp(out.beta, T_2), lw=3)
plt.plot(T_3, Exp(out.beta, T_3), 'b-' ,lw = 3)
plt.xlabel('Temperatura (C)')
plt.ylabel('Breakdown Voltage (V)')