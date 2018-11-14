import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led PID/0-20mA, step 100 uA, wait 10ms, Peltier 1V/iv/1 (iv).txt')
I_sipm = data[:, 0]
I_led = data[:, 2]
I_led_err = error_I(I_led, '2612', source=True)
I_sipm_err = error_I(I_sipm, '2400', source=False)

#%%

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

pesos = []
I_sipm_flip = np.flip(I_sipm[int(len(I_sipm)/2):-1])
for i in range(len(I_sipm[1:int(len(I_sipm)/2)])):
    pesos.append(np.max([I_sipm[i], I_sipm_flip[i]]))

dif_temp = I_sipm[1:int(len(I_sipm)/2)] - I_sipm_flip
dif = [dif_temp[i]/pesos[i] for i in range(len(dif_temp))]

plt.plot(I_led[1:int(len(I_led)/2)], dif, 'og')
plt.hist(dif, bins = 200, normed=True)
plt.xlabel(r'$I_{led} (A)$', size = 15)
plt.ylabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)
plt.grid(True)

#%%
import scipy.stats as stats
 
mean = np.mean(dif)
sigma = np.std(dif, ddof=1)
a = mean - sigma
b = mean + sigma
uniform = []
for i in range(2000):
    uniform.append(np.random.uniform(a, b))  
    
plt.figure(1)
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

plt.figure(2)
plt.hist(dif, bins = 200, normed=True)
plt.hist(c, bins = 200, normed=True)
plt.vlines(mean, 0, 200)
plt.vlines(mean + sigma, 0, 200)
plt.vlines(mean - sigma, 0, 200)
plt.xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)