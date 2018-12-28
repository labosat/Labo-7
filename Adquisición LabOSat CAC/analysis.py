from __future__ import division
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from functions import DetectFolders

#current working directory (all paths relative to this one)
os.chdir("C:/Users/lucas/Documents/GitHub/Labo-7/Adquisición LabOSat/")

#constants for data analysis

pixels = 18980
m = 3.81
R0 = 1000

encapsulado = "1 con grasa doble T"
folders = DetectFolders('results/Encapsulado %s/' % encapsulado)

#tolerance in temperature
tol = 0.1


#%% imports

from functions import tolerance, tolerance_dark, weightedMean, weightedError, error_R, error_V, error_I, Linear, ClosestToOne, LogData, DiffData, fit_calc, fit_function
from scipy.odr import ODR, Model, RealData


#%% rq analysis

Rq = []
T = []
Rq_err = []
T_err = []    

for i in range(1, folders + 1):

    path = 'results/Encapsulado %s/%s (rq)' % (encapsulado, i)

    Rq_temp = []
    T_temp = []
    Rq_err_temp = []
    T_err_temp = []
    #casa
    array = tolerance(tol, path)
    end = len(array)
    

    for j in array:
        
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
        
plt.errorbar(T, Rq, xerr=T_err, yerr=Rq_err, fmt='.k', capsize=3)
    
#%% vbr analysis

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

<<<<<<< HEAD
    path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Adquisición LabOSat/results/Encapsulado 1 con grasa/%s (vbr)' % i
=======
    path = 'results/Encapsulado %s/%s (vbr)' % (encapsulado, i)
>>>>>>> 86842c650e72e46405d8393255609f2d7a872795
    Vbr_temp = []
    T_temp = []
    Vbr_err_temp = []
    T_err_temp = []

    array = tolerance(tol, path)
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
            for h in range(l + 1, len(V[index:])):
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

I_dark = []
R_dark = []
I_dark_err = []
R_dark_err = []
for k in range(1, folders + 1):
    
    path_dark = 'results/Encapsulado %s/%s (idark)' % (encapsulado, k)

    array = tolerance_dark(tol, path_dark)
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
    

