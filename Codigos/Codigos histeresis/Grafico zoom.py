import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/results led 0-20/Estacionario 5/iv/7 (iv).txt'
data = np.loadtxt(path)
I_sipm = data[:, 0]*1000
I_led = data[:, 2]*1000
I_led_err = f.error_I(data[:, 2], '2612', source=True)
I_sipm_err = f.error_I(data[:, 0], '2400', source=False)
I_led_err = [1000*i for i in I_led_err]
I_sipm_err = [1000*i for i in I_sipm_err]

#%%
fig, ax = plt.subplots()
ax.errorbar(I_led[1:int(len(I_sipm)/2)], I_sipm[1:int(len(I_sipm)/2)], 
                   yerr=I_sipm_err[1:int(len(I_sipm)/2)], xerr=I_led_err[1:int(len(I_sipm)/2)],
                   fmt='.b', capsize = 1, label = 'Ida')
ax.errorbar(I_led[int(len(I_sipm)/2):-1], I_sipm[int(len(I_sipm)/2):-1], 
                   yerr=I_sipm_err[int(len(I_sipm)/2):-1], xerr=I_led_err[int(len(I_sipm)/2):-1],
                   fmt='.r', capsize = 1, label = 'Vuelta')
ax.set_xlabel(r'$I_{led} (mA)$', size = 15)
ax.set_ylabel(r'$I_{sipm} (\mu A)$', size = 15)
ax.grid(True)
ax.legend()
axins = zoomed_inset_axes(ax, 10, loc=4)
axins.errorbar(I_led[1:int(len(I_sipm)/2)], I_sipm[1:int(len(I_sipm)/2)], 
                   yerr=I_sipm_err[1:int(len(I_sipm)/2)], xerr=I_led_err[1:int(len(I_sipm)/2)],
                   fmt='.b', capsize = 1, label = 'Ida')
axins.errorbar(I_led[int(len(I_sipm)/2):-1], I_sipm[int(len(I_sipm)/2):-1], 
                   yerr=I_sipm_err[int(len(I_sipm)/2):-1], xerr=I_led_err[int(len(I_sipm)/2):-1],
                   fmt='.r', capsize = 1, label = 'Vuelta')
x1, x2, y1, y2 = 12.1, 12.85, 0.385, 0.41 # specify the limits
axins.set_xlim(x1, x2) # apply the x-limits
axins.set_ylim(y1, y2) # apply the y-limits
axins.set_xticks([])
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
mark_inset(ax, axins, loc1=3, loc2=4, fc="none", ec="0.5")
plt.grid(True)

#%%
fig, ax = plt.subplots()
ax.errorbar(I_led[1:int(len(I_sipm)/2)], I_sipm[1:int(len(I_sipm)/2)], 
                   yerr=I_sipm_err[1:int(len(I_sipm)/2)], xerr=I_led_err[1:int(len(I_sipm)/2)],
                   fmt='ob', capsize = 1, label = 'Ida')
ax.errorbar(I_led[int(len(I_sipm)/2):-1], I_sipm[int(len(I_sipm)/2):-1], 
                   yerr=I_sipm_err[int(len(I_sipm)/2):-1], xerr=I_led_err[int(len(I_sipm)/2):-1],
                   fmt='or', capsize = 1, label = 'Vuelta')
ax.set_xlabel(r'$I_{led} (mA)$', size = 22)
ax.set_ylabel(r'$I_{sipm} (mA)$', size = 22)
ax.grid(True)
ax.tick_params(labelsize=20)
ax.legend()

I_led_dif, I_sipm_dif = dif(I_led, I_sipm)
    
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(I_led_dif, [-i for i in I_sipm_dif], 'og')
ax1.set_xlabel(r'$I_{led} (A)$', size = 15)
ax1.set_ylabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)
ax1.grid(True)
values, bins = np.histogram([-i for i in I_sipm_dif], bins = len(I_sipm_dif))
ax2.hist(values)
ax2.set_xlabel(r'$\Delta I_{sipm} (Normalizado)$', size = 15)
ax2.set_ylabel('# Entradas', size = 15)
plt.tight_layout()