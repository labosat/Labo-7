import numpy as np
import matplotlib.pyplot as plt
from __future__ import division
import funcionesVbr as f
from scipy.optimize import curve_fit
from scipy.odr import Model, RealData, ODR
from funcionesVbr import vbr, Linear, exp, exp_inv

path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo7/Vbr en T/results/Estacionario 2'


def promediador(path, tolerancia):
    array = f.pulidor(tolerancia, path)
    celdas = 18980
    parameters = 2
    R = []
    R_err = []
    Rq = []
    Rq_err = []
    I = []
    V = []
    for h in array:
        data1 = np.loadtxt(path+'/res/%s (res).txt' % h, skiprows=1)
        Res = data1[:, 1]   
        I_res = data1[:, 2]
        V_res = I_res*Res
        V_res_err = V_res*0.00015 + 225E-6
        I_res_err = I_res*0.0003 + 60E-9
        Res_err_estadistico = f.dispersion(Res) 
        Res_err_sistematico = np.sqrt((1/I_res**2) * V_res_err**2 + ((V_res/(I_res**2))**2)*I_res_err**2)
        Res_err = np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico**2)
        R.append(f.weightedMean(Res, Res_err))
        R_err.append(f.weightedErrorR(Res, Res_err))
        
        data2 = np.loadtxt(path+'/iv/%s (iv).txt' % h, skiprows=1)
        V.append(list(data2[:, 0]))
        I.append(list(data2[:, 1]))
    
    I_promedio = []
    for i in range(len(I[1])):
        c = 0
        for j in range(len(I)):
            c += I[j][i] 
        I_promedio.append(c/len(I))
        
    V_promedio = []  
    for i in range(len(V[1])):
        c = 0
        for j in range(len(V)):
            c += V[j][i]
        V_promedio.append(c/len(V))
        
    return V_promedio, I_promedio
    
V, I = promediador(path, 0.025)
        
        
V = data2[:, 0]
I = data2[:, 1]
        
        

#        ranges = f.DetermineRange(V, I)
V_err = [(i*0.0002 + 50*pow(10, -3)) for i in V]
I_err = f.MultiRange(I)

I = [np.log(i) for i in I]
I_err = [abs((I_err[i]/I[i])) for i in range(len(I))]

V, V_err, I, I_err = f.DerivateData(V, V_err, I, I_err)

plt.errorbar(V, I, xerr=V_err, yerr=I_err, fmt='.')


chi2 = []
N = len(I)
m_temp = []
b_temp = []
m_err_temp = []
for j in range(N-2):
    I_temp = [I[i] for i in range(N-j)]
    I_temp = np.asarray(I_temp)
    V_temp = [V[i] for i in range(N-j)]
    V_temp = np.asarray(V_temp)
    V_err_temp = [V_err[i] for i in range(N-j)]
    V_err_temp = np.asarray(V_err_temp)
    I_err_temp = [I_err[i] for i in range(N-j)]
    I_err_temp = np.asarray(I_err_temp)
#        fit, _ = curve_fit(f.vbr, V_temp, I_temp, sigma=I_err_temp)
#        chi2.append(chisq/(len(I_temp)-2))
    
    linear_model = Model(Linear)
    data = RealData(V_temp, I_temp, sx=V_err_temp, sy=I_err_temp)
    odr = ODR(data, linear_model, beta0=[0., 1.])
    out = odr.run()
    m_temp.append(out.beta[0])
    b_temp.append(out.beta[1])
    m_err_temp.append(out.sd_beta[0])
    chi2.append(out.res_var)
    
chi_2 = chi2[f.ClosestToOne(chi2)]
m = m_temp[f.ClosestToOne(chi2)]
b = b_temp[f.ClosestToOne(chi2)]

plt.plot(V, [m*V[i]+b for i in range(len(V))])
plt.errorbar(V, I, xerr=V_err, yerr=I_err, fmt='.')


#%%

exp_model = Model(exp)
data = RealData(V, I, sx=V_err, sy=I_err)
odr = ODR(data, exp_model, beta0=[0.5, 1., 0.05])
out = odr.run()

a_temp = out.beta[0]
b_temp = out.beta[1]
c_temp = out.beta[2]
m_err_temp = out.sd_beta[0]
chi2 = out.res_var

plt.figure(3)
plt.plot(V, [(a_temp * np.exp(b_temp * V[i])) for i in range(len(V))])
plt.errorbar(V, I, yerr=I_err, xerr=V_err, fmt='.')
plt.grid(True)
#plt.yscale('log')
plt.xlabel('Voltage (V)')
plt.ylabel('Current (A)')
    