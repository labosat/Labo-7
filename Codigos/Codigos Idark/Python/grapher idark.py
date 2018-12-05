import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import ODR, Model, RealData

data = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones/Graficos y txt/txts/data_dark.txt', skiprows=1)
I = data[:, 1]
dI = data[:, 2]
R = data[:, 3]
dR = data[:, 4]

def Linear(M, x):
    m, b = M
    return m*x + b

#%% AJUSTE EL PRIMER RANGO LINEAL

T = [(i-1000)/3.815 for i in R]
dT = [i/3.815 for i in dR]

linear_model = Model(Linear)
data = RealData(T[0:13], np.log(I[0:13]), sx=dT[:13], 
                sy=[dI[0:13][i] / I[0:13][i] for i in range(13)])
odr = ODR(data, linear_model, beta0=[0., 1.])
out = odr.run()
    
m = out.beta[0]
b = out.beta[1]
m_err = out.sd_beta[0]
b_err = out.sd_beta[1]        
chi2 = out.res_var



plt.figure(1)
plt.errorbar(T, np.log(I), xerr=dT, yerr=[dI[i] / I[i] for i in range(len(I))], fmt='sk', capsize=3)
plt.grid(True)
plt.plot(T[0:13], [m*i + b for i in T[0:13]], 'b--', lw = 2)
plt.xlabel('Temperatura (C)', size=22)
plt.ylabel('Dark Current (log(A))', size=22)
plt.tick_params(labelsize=22)
plt.axvspan(-35, 7, alpha=0.5, color='red')
plt.text(-30, -13, 'Linear region', fontsize=25)
#%%  AJUSTE TODO EL RANGO

T = [(i-1000)/3.815 for i in R]
dT = [i/3.815 for i in dR]

def Linear(M, x):
    m, b = M
    return m*x + b

linear_model = Model(Linear)
data = RealData(T, np.log(I), sx=dT, 
                sy=[dI[i] / I[i] for i in range(len(I))])
odr = ODR(data, linear_model, beta0=[0., 1.])
out = odr.run()
    
m = out.beta[0]
b = out.beta[1]
m_err = out.sd_beta[0]
b_err = out.sd_beta[1]        
chi2 = out.res_var



plt.figure(2)
plt.errorbar(T, np.log(I), xerr=dT, yerr=[dI[i] / I[i] for i in range(len(I))], fmt='sk', capsize=3)
plt.grid(True)
plt.plot(T, [m*i + b for i in T], 'r--', lw = 2)
plt.xlabel('Temperatura (C)', size=22)
plt.ylabel('Dark Current (log(A))', size=22)
plt.tick_params(labelsize=22)

plt.figure(3)
plt.errorbar(T, I, xerr=dT, yerr=dI, fmt='sk', capsize=3)
plt.plot(np.arange(-35.5, 35.5, 0.1), [np.exp(m*i+b) for i in np.arange(-35.5, 35.5, 0.1)], 'r--', lw=2)
plt.xlabel('Temperatura (C)', size=22)
plt.ylabel('Dark Current (A)', size=22)
plt.tick_params(labelsize=22)
plt.grid(True)

#%% AJUSTE CON TODOS LOS DATOS
import numpy as np
import matplotlib.pyplot as plt
import Funciones as f

I_dark = []
R = []
I_dark_err = []
R_err = []
for i in range(1, 20):
    path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones/Vbr/Para informe/Vbr/Estacionario %s' % i
    array = f.pulidor(0.03, path)
    I_dark_temp = []
    R_temp = []
    I_dark_err_temp = []
    R_err_temp = []
    for j in array:
        dataR = np.loadtxt(path + '/res/%s (res).txt' % j, skiprows=1)
        data = np.loadtxt(path + '/iv/%s (iv).txt' %j)
        I_dark.append(data[:, 1][np.where(data[:, 0] == 30.)[0][0]])
        R.append(dataR[:, 1][np.where(data[:, 0] == 30.)[0][0]])
        
I_dark_err = f.error_I(I_dark, '2612')
R_err = f.error_R(R, 0.000097)

T = [(i-1000)/3.815 for i in R]
dT = [i/3.815 for i in R_err]

def Linear(M, x):
    m, b = M
    return m*x + b

linear_model = Model(Linear)
data = RealData(T, np.log(I_dark), sx=dT, 
                sy=[I_dark_err[i] / I_dark[i] for i in range(len(I_dark))])
odr = ODR(data, linear_model, beta0=[0., 1.])
out = odr.run()
    
m = out.beta[0]
b = out.beta[1]
m_err = out.sd_beta[0]
b_err = out.sd_beta[1]        
chi2 = out.res_var


plt.errorbar(T, I_dark, xerr=dT, yerr=I_dark_err, fmt='.k', capsize=3)
plt.plot(np.arange(-35.5, 42, 0.1), [np.exp(m*i+b) for i in np.arange(-35.5, 42, 0.1)], 'r--', lw=2)
plt.xlabel('Temperatura (C)', size=22)
plt.ylabel('Dark Current (A)', size=22)
plt.tick_params(labelsize=22)
plt.grid(True)