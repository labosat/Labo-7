from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from Funciones import Linear
import sys
sys.path.append('./Labo-7/')
from scipy.odr import Model, RealData, ODR
from scipy import integrate

path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/hist_vs_wait_time(0-200)'


I_sipm = []
I_sipm_err = []
I_led_err = []
I_led = []
for i in ['1e-7', '1e-6', '1e-5','0.0001', '0.001', '0.01', '0.025', '0.05', '0.075', '0.1']:
        data = np.loadtxt(path + '/' + str(i) + '/iv/1 (iv).txt', skiprows=1)
        I_sipm.append(data[:, 0])
        I_led.append(data[:, 2])        
        I_sipm_err.append(f.error_I(data[:, 0], '2400'))
        I_led_err.append(f.error_I(data[:, 2], '2612'))
        #V_err.append(f.error_V(data[:, 0]))
        
distancias = []
for i in range(len(I_sipm)):
    d = [(I_sipm[i][len(I_sipm[i])-1 - j] - I_sipm[i][j]) for j in range(int(len(I_sipm[i])/2))]
    distancias.append(d)

d_max = []
for i in range(len(distancias)):
    d_max.append(np.max(distancias[i]))
    
plt.figure(1)
plt.plot([1e-7, 1e-6, 1e-5, 0.0001, 0.001, 0.01, 0.025, 0.05, 0.075, 0.1], d_max, 'o')
plt.xlabel('Wait Time (s)')
plt.ylabel('Histeresis area')

#for i in range(len(['1e-7', '1e-6', '1e-5','0.0001', '0.001', '0.01', '0.025', '0.05', '0.075', '0.1'])):
#    plt.plot(I_led[i], I_sipm[i], '.')
    
areas = []
for i in range(len(I_sipm)):
    I_sipm_temp_1 = I_sipm[i][:int(len(I_sipm[i])/2)]
    I_led_temp_1 = I_led[i][:int(len(I_led[i])/2)]
    I_sipm_temp_2 = I_sipm[i][int(len(I_sipm[i])/2):]
    I_led_temp_2 = I_led[i][int(len(I_led[i])/2):]
    area = integrate.simps(I_sipm_temp_1, I_led_temp_1) - integrate.simps(I_sipm_temp_2, I_led_temp_2)  
    areas.append(area)

plt.figure(2)
plt.loglog([1e-7, 1e-6, 1e-5, 0.0001, 0.001, 0.01, 0.025, 0.05, 0.075, 0.1], areas, 'o')
plt.xlabel('Wait Time (s)')
plt.ylabel('Histeresis area')    
    

data = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Wait Time/medicion rq/wait_time_vs_rq.txt', skiprows=1)
Rq = data[:, 0]
Rq_err = data[:, 1]
wait_time = data[:, 4]

plt.figure(3)
plt.plot(wait_time, Rq, 'o')
plt.errorbar(wait_time, Rq, yerr=Rq_err, fmt='ok', capsize=5)
plt.xscale('log')
plt.grid(True)
plt.xlabel('Wait Time (s)', fontsize = 20)
plt.ylabel(r'$R_q$ ($\Omega$)', fontsize = 20)
