import numpy as np
import matplotlib.pyplot as plt
import Funciones as f


path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/results led PID/0-20mA, step 25 uA, wait 10ms, bis bis/iv/1 (iv).txt'

data = np.loadtxt(path)
I_sipm = data[:, 0]
I_led = data[:, 2]
I_led_err = f.error_I(I_led, '2612', source=True)
I_sipm_err = f.error_I(I_sipm, '2400', source=False)

def dif(x, y):
    ''' Esta funcion agarra una curva ida y vuelta (con mismo eje x), y calcula la 
    diferencia entre la ida y la vuelta para cada x, normalizado por el maximo del par.'''
    pesos = []
    y_flip = np.flip(y[int(len(y)/2):-1], axis=0)
    for i in range(len(y[1:int(len(y)/2)])):
        pesos.append(np.max([y[i], y_flip[i]]))
    
    dif_temp = y[1:int(len(y)/2)] - y_flip
    y_dif = [dif_temp[i]/1 for i in range(len(dif_temp))] #pesos[i] en 1
    x_dif = x[1:int(len(x)/2)]
    return x_dif, y_dif
#%% 
'''Plot de diferencias entre curva de subida y de bajada normalizadas.'''

plt.figure(1)
plt.errorbar(I_led[1:int(len(I_sipm)/2)]*1000, 1000*I_sipm[1:int(len(I_sipm)/2)], 
                   yerr=1000*np.asarray(I_sipm_err[1:int(len(I_sipm)/2)]), xerr=1000*np.asarray(I_led_err[1:int(len(I_sipm)/2)]),
                   fmt='.b', capsize = 1, label = 'Ida')
plt.errorbar(1000*I_led[int(len(I_sipm)/2):-1], 1000*I_sipm[int(len(I_sipm)/2):-1], 
                   yerr=1000*np.asarray(I_sipm_err[int(len(I_sipm)/2):-1]), xerr=1000*np.asarray(I_led_err[int(len(I_sipm)/2):-1]),
                   fmt='.r', capsize = 1, label = 'Vuelta')
#plt.plot(I_led[1:int(len(I_sipm)/2)], I_sipm[1:int(len(I_sipm)/2)], '.', label = 'Ida')
#plt.plot(I_led[int(len(I_sipm)/2):-1], I_sipm[int(len(I_sipm)/2):-1], '.', label = 'Vuelta')
plt.xlabel(r'$I_{led} (mA)$', size = 15)
plt.ylabel(r'$I_{sipm} (mA)$', size = 15)
plt.legend()
plt.grid(True)
plt.yscale('log')
plt.xscale('log')
plt.scatter(11.3, 0.355)

I_led_dif, I_sipm_dif = dif(I_led, I_sipm)
I_sipm_err_dif = [np.sqrt(I_sipm_err[1:int(len(I_sipm)/2)][i]**2 - I_sipm_err[int(len(I_sipm)/2):-1][i]**2) for i in range(len(I_sipm_err[int(len(I_sipm)/2):-1]))]
    
fig, (ax1, ax2) = plt.subplots(2, 1)
#ax1.plot(I_led_dif, [-i*10**3 for i in I_sipm_dif], 'og')
ax1.errorbar(I_led_dif, [-i*10**3 for i in I_sipm_dif],xerr=f.error_I(I_led_dif, '2612', source=True), yerr=[i*10**3 for i in I_sipm_err_dif], fmt='og', capsize=3)
ax1.set_xlabel(r'$I_{led} (mA)$', size = 15)
ax1.set_ylabel(r'$\Delta I_{sipm} (mA)$', size = 15)
ax1.grid(True)
values, bins = np.histogram(I_sipm_dif, bins = len(I_sipm_dif))
m, bins, _ = ax2.hist([-i*10**3 for i in I_sipm_dif], bins=10)
#ax2.plot(bins[:-1], values, lw=2)
ax2.set_xlabel(r'$\Delta I_{sipm} (mA)$', size = 15)
ax2.set_ylabel('# Entradas', size = 15)
bins_err = bins + (bins[2] - bins[1])/2
ax2.errorbar(bins_err[:-1], m, yerr = [np.sqrt(i) for i in m], fmt = '.r', capsize = 3)
plt.tight_layout()
#%%
''' Simulacion de datos gaussianos y uniformes para comparar con lo medido'''

import scipy.stats as stats
 
print('')
print('Test para datos sin filtro.')

mean = np.mean(I_sipm_dif)
sigma = np.std(I_sipm_dif, ddof=1)
a = mean - sigma
b = mean + sigma
uniform = []
for i in range(20000):
    uniform.append(np.random.uniform(a, b))  
    
plt.figure(4)
plt.hist(I_sipm_dif, bins = 200, normed=True)
plt.hist(uniform, bins = 200, normed=True)
plt.vlines(mean, 0, 100)
plt.vlines(mean + sigma, 0, 100)
plt.vlines(mean - sigma, 0, 100)
plt.xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)

print('')
print('Test de Kolmogorov-Smirnov para una muestra uniforme' +
      ' y los datos: ')
print('p-value = ' + str(stats.ks_2samp(uniform, I_sipm_dif)[1]))

c = []
for i in range(100000):
    c.append(stats.norm.rvs(loc = mean, scale = sigma))

plt.figure(5)
plt.hist(I_sipm_dif, bins = 200, normed=True)
plt.hist(c, bins = 800, normed=True)
plt.vlines(mean, 0, 200)
plt.vlines(mean + sigma, 0, 200)
plt.vlines(mean - sigma, 0, 200)
plt.xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)

print('')
print('Test de Kolmogorov-Smirnov para una muestra gaussiana' +
      ' y los datos: ') 
print('p-value = ' + str(stats.ks_2samp(c, I_sipm_dif)[1]))
#%%
# Pruebo hacer el mismo analisis filtrando los datos que se alejan mucho de la curva
# Criterio: me quedo solo con la nube de puntos alrededor del 0.
print('')
print('Test para datos filtrados dentro del primer sigma.')

mean = np.mean(I_sipm_dif)
sigma = np.std(I_sipm_dif, ddof=1)
dif_filtro = []
led_filtro = []
for i in range(len(I_sipm_dif)):
    if I_sipm_dif[i] < mean + sigma and I_sipm_dif[i] > mean - sigma: #el 0.005 viene de 
        dif_filtro.append(I_sipm_dif[i])                              #quedarme con la nube
        led_filtro.append(I_led_dif[i])                               #de puntos de
                                                                      #alrededor del 0.

fig2, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(led_filtro, dif_filtro, 'og')
ax1.set_xlabel(r'$I_{led} (A)$', size = 15)
ax1.set_ylabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)
ax1.grid(True)
values, bins = np.histogram(dif_filtro, bins = len(dif_filtro))
ax2.plot(bins[:-1], values, lw=2)
ax2.set_xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)
ax2.set_ylabel('# Entradas', size = 15)
plt.tight_layout()

mean = np.mean(dif_filtro)
sigma = np.std(dif_filtro)
a = mean - sigma
b = mean + sigma
uniform = []
for i in range(20000):
    uniform.append(np.random.uniform(a, b))  

bins = np.linspace(np.min(dif_filtro), np.max(dif_filtro), 100)
plt.figure(6)
plt.hist(dif_filtro, bins = bins, normed=True)
plt.hist(uniform, bins = bins, normed=True)
plt.vlines(mean, 0, 100)
plt.vlines(mean + sigma, 0, 100)
plt.vlines(mean - sigma, 0, 100)
plt.xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)

print('')
print('Test de Kolmogorov-Smirnov para una muestra uniforme' +
      ' y los datos: ')
print('p-value = ' + str(stats.ks_2samp(uniform, dif_filtro)[1]))

c = []
for i in range(20000):
    c.append(stats.norm.rvs(loc = mean, scale = sigma))

plt.figure(7)
plt.hist(dif_filtro, bins = bins, normed=True)
plt.hist(c, bins = bins, normed=True)
plt.vlines(mean, 0, 200)
plt.vlines(mean + sigma, 0, 200)
plt.vlines(mean - sigma, 0, 200)
plt.xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)

print('')
print('Test de Kolmogorov-Smirnov para una muestra gaussiana' +
      ' y los datos: ') 
print('p-value = ' + str(stats.ks_2samp(c, dif_filtro)[1]))

#%%
##import time
#pvalue = []
#for i in range(5000):
##    t0 = time.time()
#    c = []
#    for i in range(10000):
#        c.append(stats.norm.rvs(loc = mean, scale = sigma))
#    pvalue.append(stats.ks_2samp(c, dif_filtro)[1])
##    print(time.time() - t0)
#m, bins, _ = plt.hist(pvalue, bins = 50)
#bins_err = bins + (bins[2] - bins[1])/2
#plt.errorbar(bins_err[:-1], m, yerr = [np.sqrt(i) for i in m], fmt = '.r', capsize = 3)
#plt.xlabel('Pvalues', size = 15)
#plt.ylabel('# Entradas', size = 15)
