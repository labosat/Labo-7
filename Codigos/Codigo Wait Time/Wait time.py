from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from Funciones import Linear
import sys
sys.path.append('./Labo-7/')
from scipy.odr import Model, RealData, ODR

path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Wait Time/results led'

I = []
V = []
I_err = []
V_err = []
for i in ['1e-7', '1e-6', '1e-5','0.0001', '0.001', '0.01', '0.025', '0.05', '0.075', '0.1']:
        data = np.loadtxt(path + '/' + str(i) + '/iv/1 (iv).txt', skiprows=1)
        I.append(data[:, 0])
        #V.append(data[:, 0])        
        I_err.append(f.error_I(data[:, 0]))
        #V_err.append(f.error_V(data[:, 0]))
        
distancias = []
for i in range(len(I)):
    d = [(I[i][len(I[i])-1 - j] - I[i][j]) for j in range(int(len(I[i])/2))]
    distancias.append(d)
    


d_max = []
for i in range(len(distancias)):
    d_max.append(np.max(distancias[i]))
    
plt.plot([1e-7, 1e-6, 1e-5,0.0001, 0.001, 0.01, 0.025, 0.05, 0.075, 0.1], d_max, 'o')
