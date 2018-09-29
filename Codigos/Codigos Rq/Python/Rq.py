from __future__ import division
import numpy as np
from scipy.odr import Model, RealData, ODR
import matplotlib.pyplot as plt
import funcionesR as f
from funcionesR import Linear


numero_grupos = ['0.1', '0.01', '0.001', '0.0001', '0.05', '0.025', '0.075', '1e-5', '1e-6', '1e-7']
path_grupos = '/home/labosat/Desktop/Finazzi-Ferreira/Wait Time Multiple (rq)'
Rq_final = []
R_final = []
R_err_final = []
Rq_err_final = []
for i in numero_grupos:
    R, R_err, Rq, chi2, array, Rq_err = R_Rq(path_grupos + '/%s' % i, 0.02 )
    Rq_final.append(np.mean(Rq))
    R_final.append(f.weightedMean(R, R_err))
    R_err_final.append(f.weightedError(R, R_err))
    Rq_err_final.append(np.mean(Rq_err))
#    np.savetxt('array %s.txt' % i, array)
#    
#np.savetxt('R.txt', R_final)
#np.savetxt('Rerr.txt', R_err_final)

T = [(R_final[i]-1000)/3.815 for i in range(len(R_final))]
T_err = [R_err_final[i]/3.815 for i in range(len(R_err_final))]

plt.figure(1)
plt.plot(T, Rq_final, 'o')
plt.errorbar(x=T, y=Rq_final, xerr=T_err, yerr=Rq_err_final, fmt='none')
plt.xlabel('Temperatura (C)')
plt.ylabel('Rq (Ohms)')

wait_time = [0.1, 0.01, 0.001, 0.0001, 0.05, 0.025, 0.075, 1e-5, 1e-6, 1e-7]
plt.figure(2)
plt.plot(wait_time, Rq_final, 'o')
plt.xscale('log')
plt.errorbar(wait_time, Rq_final, yerr=Rq_err_final, fmt='none')
plt.xlabel('Wait time (s)')
plt.ylabel('Rq (Ohms)')
#%%
R_totals = []
Rq_totals = []
for i in range(1, numero_grupos):
    R, R_err, Rq, chi2, array = R_Rq(path_grupos + 'Estacionario %s' % i, 0.02 )
    R_totals.append(R)
    Rq_totals.append(Rq)

#R, R_err, Rq, chi2 = R_Rq('/home/labosat/Desktop/Finazzi-Ferreira/Labo7/Rq en T/Running 1', 0.03)

##Aca aplano las listas. Paso de lista de listas a un solo array
R_total = [item for sublist in R_totals for item in sublist]
Rq_total = [item for sublist in Rq_totals for item in sublist]


plt.plot(R_total, Rq_total, '.')
#plt.hist(R_totals[2], bins=100)
#np.savetxt('Rq.txt', Rq)
#np.savetxt('chi2.txt', chi2_out)
#        

#%%
#Esto sirve para comparar graficos de puntos especificos y estudiar en
#detalle los escalones.

for i in (72, 73, 74, 75, 76, 77):
        data = np.loadtxt(path+'/res/%s (res).txt' % i, skiprows=1)
        R = data[:, 1]
        data = np.loadtxt(path+'/iv/%s (iv).txt' % i, skiprows=1)
        V = data[:, 0]
        I = data[:, 1]
        plt.figure(1)
        plt.plot(R, '.')
        
        plt.figure(2)
        plt.plot(V, I, '.')
    
#%%
#data = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo7/Rq en T/Running 1/res/91 (res).txt', skiprows=1)
#R = data[:, 1]
#plt.plot(R, '.')
#print(f.dispersion(R))
        
for i in range():
    R, R_err, Rq, chi2, array = R_Rq(path_grupos + 'Estacionario %s' % i, 0.03 )
