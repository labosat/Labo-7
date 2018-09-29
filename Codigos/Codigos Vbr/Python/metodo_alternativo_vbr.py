from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from Funciones import Linear



data = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones_temporarias/Vbr/Estacionario 15/iv/17 (iv).txt')
V = data[1:, 0]
I = data[1:, 1] 
V_err = f.error_V(V)
I_err = f.error_I(I)

m, b, ks_stat, index = f.ks_iterative(V, I, V_err, I_err)

plt.plot(V, I, '.')
plt.errorbar(V, I, yerr=I_err, xerr=V_err, fmt='none')
plt.plot(V, V*m+b, lw = 3)



sigma = f.dispersion(I[1:len(V)-index])

k = 0
for i in range(len(V[1:])):
    if abs(I[i]) > abs((m*V[i] + b) + 2*sigma):
        print V[i]
        k = i
        break
print 'El voltaje de ruptura es %sV aprox.' % V[k] 

plt.plot(V, I, '.')
plt.errorbar(V, I, yerr=I_err, xerr=V_err, fmt='none')
plt.plot(V, V*m+b, lw = 3)
plt.plot(V[k], I[k], 'o')