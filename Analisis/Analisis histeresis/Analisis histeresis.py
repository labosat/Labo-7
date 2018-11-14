import numpy as np
import matplotlib.pyplot as plt
import Funciones as f

path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/results led PID/0-20mA, step 100 uA, wait 10ms, Peltier 12V bis bis/iv/1 (iv).txt'
data = np.loadtxt(path)
I_sipm = data[:, 0]
I_led = data[:, 2]
I_led_err = f.error_I(I_led, '2612', source=True)
I_sipm_err = f.error_I(I_sipm, '2400', source=False)

def dif(x, y):
    ''' Esta funcion agarra una curva ida y vuelta (con mismo eje x), y calcula la 
    diferencia entre la ida y la vuelta para cada x, normalizado por el maximo del par.'''
    pesos = []
    y_flip = np.flip(y[int(len(y)/2):-1])
    for i in range(len(y[1:int(len(y)/2)])):
        pesos.append(np.max([y[i], y_flip[i]]))
    
    dif_temp = y[1:int(len(y)/2)] - y_flip
    y_dif = [dif_temp[i]/pesos[i] for i in range(len(dif_temp))]
    x_dif = x[1:int(len(x)/2)]
    return x_dif, y_dif
#%% 
'''Plot de diferencias entre curva de subida y de bajada normalizadas.'''

plt.figure(1)
plt.errorbar(I_led[1:int(len(I_sipm)/2)], I_sipm[1:int(len(I_sipm)/2)], 
                   yerr=I_sipm_err[1:int(len(I_sipm)/2)], xerr=I_led_err[1:int(len(I_sipm)/2)],
                   fmt='.b', capsize = 1, label = 'Ida')
plt.errorbar(I_led[int(len(I_sipm)/2):-1], I_sipm[int(len(I_sipm)/2):-1], 
                   yerr=I_sipm_err[int(len(I_sipm)/2):-1], xerr=I_led_err[int(len(I_sipm)/2):-1],
                   fmt='.r', capsize = 1, label = 'Vuelta')
#plt.plot(I_led[1:int(len(I_sipm)/2)], I_sipm[1:int(len(I_sipm)/2)], '.', label = 'Ida')
#plt.plot(I_led[int(len(I_sipm)/2):-1], I_sipm[int(len(I_sipm)/2):-1], '.', label = 'Vuelta')
plt.xlabel(r'$I_{led} (A)$', size = 15)
plt.ylabel(r'$I_{sipm} (A)$', size = 15)
plt.legend()
plt.grid(True)

I_led_dif, I_sipm_dif = dif(I_led, I_sipm)
    
plt.figure(2)
plt.plot(I_led_dif, I_sipm_dif, 'og')
#plt.hist(dif, bins = 200, normed=True)
plt.xlabel(r'$I_{led} (A)$', size = 15)
plt.ylabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)
plt.grid(True)

#%%
''' Simulacion de datos gaussianos y uniformes para comparar con lo medido'''

import scipy.stats as stats
 
mean = np.mean(dif)
sigma = np.std(dif, ddof=1)
a = mean - sigma
b = mean + sigma
uniform = []
for i in range(2000):
    uniform.append(np.random.uniform(a, b))  
    
plt.figure(3)
plt.hist(dif, bins = 200, normed=True)
plt.hist(uniform, bins = 200, normed=True)
plt.vlines(mean, 0, 100)
plt.vlines(mean + sigma, 0, 100)
plt.vlines(mean - sigma, 0, 100)
plt.xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)
#stats.ks_2samp()



c = []
for i in range(2000):
    c.append(stats.norm.rvs(loc = mean, scale = sigma))

plt.figure(4)
plt.hist(dif, bins = 200, normed=True)
plt.hist(c, bins = 200, normed=True)
plt.vlines(mean, 0, 200)
plt.vlines(mean + sigma, 0, 200)
plt.vlines(mean - sigma, 0, 200)
plt.xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)

#%%

