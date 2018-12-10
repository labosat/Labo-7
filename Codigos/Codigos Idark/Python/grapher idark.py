import numpy as np
import matplotlib.pyplot as plt
import Funciones as f


R = []
R_err = []
for i in range(1, 8):
    path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/results led 0-20/Estacionario %s' % i
    dataR = np.loadtxt(path + '/res/2 (res).txt', skiprows=1)
    data = np.loadtxt(path + '/iv/2 (iv).txt')
    I_sipm = data[:int(len(data[:, 0])/2), 0]
    I_led = data[:int(len(data[:, 2])/2), 2]
    R.append(np.mean(dataR[:, 1]))
    I_sipm_err = f.error_I(I_sipm, '2400', source=False)
    I_led_err = f.error_I(I_led, '2612', source=True)
    R_err = f.error_R(R, 0.000097)
    plt.errorbar(I_led, I_sipm, xerr=I_led_err, yerr=I_sipm_err, fmt='s', capsize=3)

    
T = [(i-1000)/3.815 for i in R]
dT = [i/3.815 for i in R_err]

plt.errorbar(T, I_dark, xerr=dT, yerr=I_dark_err, fmt='.k', capsize=3)
plt.plot(np.arange(-35.5, 42, 0.1), [np.exp(m*i+b) for i in np.arange(-35.5, 42, 0.1)], 'r--', lw=2)
plt.xlabel('Temperatura (C)', size=22)
plt.ylabel('Dark Current (A)', size=22)
plt.tick_params(labelsize=22)
plt.grid(True)