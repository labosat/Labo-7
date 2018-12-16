import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
import scipy.stats as stats


def dif(x, y):
    ''' Esta funcion agarra una curva ida y vuelta (con mismo eje x), y calcula la 
    diferencia entre la ida y la vuelta para cada x, normalizado por el maximo del par.'''
    pesos = []
    y_flip = np.flip(y[int(len(y)/2.):-1], axis=0)
    for i in range(len(y[1:int(len(y)/2.)])):
        pesos.append(np.max([y[i], y_flip[i]]))
    
    dif_temp = y[1:int(len(y)/2.)] - y_flip
    y_dif = [dif_temp[i] for i in range(len(dif_temp))] #pesos[i] en 1
    x_dif = x[1:int(len(x)/2.)]
    return x_dif, y_dif

path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Labosat Medicion/results/Mediciones autocalentamiento/Mediciones autocalentamiento 4/'
#%%
# Analisis clasico de histeresis para todo el grupo de mediciones

I_sipm_dif = []
I_led_dif = []
I_sipm_err_dif = []

j = 1
while True:
    try:
        data = np.loadtxt(path + '%s.txt' % j, skiprows=1)
        if len(data[:int(len(data[:, 0])/2), 0]) == len(data[int(len(data[:, 0])/2):, 1]):
            I_sipm = data[:, 1]
            I_led = data[:, 3]
        
            I_led_err = f.error_I(I_led, '2612', source=True)
            I_sipm_err = f.error_I(I_sipm, '2612', source=False)
            I_led_dif_temp, I_sipm_dif_temp = dif(I_led, I_sipm)
            I_sipm_dif.append(I_sipm_dif_temp)
            I_led_dif.append( I_led_dif_temp)
            I_sipm_err_dif.append([np.sqrt(I_sipm_err[1:int(len(I_sipm)/2.)][i]**2 - I_sipm_err[int(len(I_sipm)/2.):-1][i]**2) for i in range(len(I_sipm_err[int(len(I_sipm)/2.):-1]))])
            print(j)
        else:
            I_sipm = data[:-1, 1]
            I_led = data[:-1, 3]
        
            I_led_err = f.error_I(I_led, '2612', source=True)
            I_sipm_err = f.error_I(I_sipm, '2612', source=False)
            I_led_dif_temp, I_sipm_dif_temp = dif(I_led, I_sipm)
            I_sipm_dif.append(I_sipm_dif_temp)
            I_led_dif.append( I_led_dif_temp)
            I_sipm_err_dif.append([np.sqrt(I_sipm_err[1:int(len(I_sipm)/2.)][i]**2 - I_sipm_err[int(len(I_sipm)/2.):-1][i]**2) for i in range(len(I_sipm_err[int(len(I_sipm)/2.):-1]))])
            print(j)
        j += 1
    except IOError:
        break
        
        
I_sipm_delta = [item for sublist in I_sipm_dif for item in sublist]
I_sipm_err_delta = [item for sublist in I_sipm_err_dif for item in I_sipm_dif]
fig, (ax1, ax2) = plt.subplots(2, 1)

for k in range(len(I_sipm_dif)):
    x_err = f.error_I(I_led_dif[k], '2612', source=True)
    ax1.plot(1000*I_led_dif[k], [-i*10**3 for i in I_sipm_dif[k]], 'og')
    ax1.errorbar(1000*I_led_dif[k], [-i*10**3 for i in I_sipm_dif[k]],
                 xerr=[1000*i for i in x_err],
                 yerr=[i*10**3 for i in I_sipm_err_dif[k]], fmt='og', capsize=3)

ax1.set_xlabel(r'$I_{led} [mA]$', size = 20)
ax1.set_ylabel(r'$\Delta I_{sipm} [mA]$', size = 20)
ax1.tick_params(labelsize=20)
ax1.set_xscale('log')
ax1.grid(True)
values, bins = np.histogram(I_sipm_delta, bins = np.linspace(-0.0005, 0.0018, 150))# len(I_sipm_delta))
m, bins, _ = ax2.hist([-i*10**3 for i in I_sipm_delta], bins = np.linspace(-0.0005, 0.0018, 150))  #150)
#ax2.plot(bins[:-1], values, lw=2)
ax2.set_xlabel(r'$\Delta I_{sipm} [mA]$', size = 20)
ax2.set_ylabel('# Entradas', size = 20)
bins_err = bins + (bins[2] - bins[1])/2
ax2.errorbar(bins_err[:-1], m, yerr = [np.sqrt(i) for i in m], fmt = '.r', capsize = 3)
ax2.tick_params(labelsize=20)


#%%
#Hago el analisis de los pvalues en funcion de la corriente del LED para una sola curva.
pvalues = []
data = np.loadtxt(path + '%s.txt' % 5, skiprows=1)
I_led_delta, I_sipm_delta = dif(data[:, 3], data[:, 1])
for k in range(2, len(I_sipm_delta)):    
    values = []
    succeses = 0
    for i in I_sipm_delta[:k]:
        if i > 0:
            values.append(1)
            succeses += 1
        elif i < 0:
            values.append(0)
    N = len(values)
    pvalues.append(stats.binom_test(succeses, N, p=0.5))
I_led = [1000*i for i in I_led_delta[2:]]
plt.plot(I_led, pvalues, 'o')
plt.plot(I_led, [0.05 for i in range(len(I_led))], 'r', lw=2.5, label='0.05')
plt.xlabel(r'$I_{led} [mA]$', size = 20)
plt.ylabel(r'P-values', size=20)
plt.tick_params(labelsize=20)
plt.xscale('log')
plt.grid(True)
plt.legend()
#%%
#Hago el analisis de los pvalues en funcion de la corriente del LED para todos los grupos.
pvalues = []

j = 1
while True:
    try:
        pvalues_temp = []
        data = np.loadtxt(path + '%s.txt' % j, skiprows=1)
        I_led_delta, I_sipm_delta = dif(data[:, 3], data[:, 1])
        for k in range(2, len(I_sipm_delta)):    
            values = []
            succeses = 0
            for i in I_sipm_delta[:k]:
                if i > 0:
                    values.append(1)
                    succeses += 1
                elif i < 0:
                    values.append(0)
            N = len(values)
            pvalues_temp.append(stats.binom_test(succeses, N, p=0.5))
        pvalues.append(pvalues_temp)
        j += 1
    except IOError:
        break
I_led = [1000*i for i in I_led_delta[2:]]


#calculo el promedio para cada punto del LED
pvalues_mean = []
pvalues_mean_err = []
for i in range(len(pvalues[1])):
    m = []
    for k in range(len(pvalues)):
        m.append(pvalues[k][i])
    pvalues_mean.append(np.mean(m))
    pvalues_mean_err.append(np.std(m))
    
plt.errorbar(I_led, pvalues_mean, yerr=pvalues_mean_err, fmt = 'o', capsize=3)
plt.plot(I_led, [0.05 for i in range(len(I_led))], 'r', lw=2.5, label='0.05')
plt.xlabel(r'$I_{led} [mA]$', size = 20)
plt.ylabel(r'P-values', size=20)
plt.tick_params(labelsize=20)
plt.xscale('log')
plt.grid(True)