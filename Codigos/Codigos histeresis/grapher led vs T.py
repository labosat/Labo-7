import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
#%%

R = []
R_err = []
colors = ['sb', 'sm', 'sg', 'sr', 'sk', 'sc']
for i in [1, 3, 4, 5, 7]:
    path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/results led 0-20/Estacionario %s' % i
    dataR = np.loadtxt(path + '/res/2 (res).txt', skiprows=1)
    data = np.loadtxt(path + '/iv/2 (iv).txt')
    I_sipm = data[1:int(len(data[:, 0])/2), 0]
    I_led = data[1:int(len(data[:, 2])/2), 2]
    R = dataR[:, 1]
    R_err = f.error_R(R, 0.000097)
    R_err = np.linalg.norm(R_err) / np.sqrt(len(R_err))
    T = (np.mean(R) - 1000)/3.815
    T_err = R_err/3.815
    I_sipm_err = f.error_I(I_sipm, '2400', source=False)
    I_led_err = f.error_I(I_led, '2612', source=True)
    I_led = 1000*I_led
    I_led_err = [1000*i for i in I_led_err]
    I_sipm = 1000*I_sipm
    I_sipm_err = [1000*i for i in I_sipm_err]
    plt.errorbar(I_led, I_sipm, xerr=I_led_err, yerr=I_sipm_err, fmt='s', capsize=3, label = r'(%s ± %s)°C' % (round(T, 2), round(T_err, 2)))

#plt.yscale('log')
#plt.xscale('log')
plt.xlabel(r'$I_{LED}$ [mA]', size=22)
plt.ylabel(r'$I_{SiPM}$ [mA]', size=22)
plt.tick_params(labelsize=22)
plt.grid(True)
plt.legend()
plt.show()


#T = [(i-1000)/3.815 for i in R]
#dT = [i/3.815 for i in R_err]

