import matplotlib.pyplot as plt
import numpy as np

#%%
data = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led PID/0-188mA, step 1mA, wait 10ms/iv/1 (iv).txt')
I_sipm = data[:, 0]
I_led = data[:, 2]
V_led = data[:, 1]

I_led_err = error_I(I_led, '2400', source = True)
I_sipm_err = error_I(I_sipm, '2612', source = False)


plt.figure(1)
plt.errorbar(I_led, I_sipm,  xerr = I_led_err, yerr=I_sipm_err, fmt ='k.', capsize = 3)
plt.xlabel(r'$I_{led}$ (A)', size = 15)
plt.ylabel(r'$I_{sipm}$ (A)', size = 15)
plt.grid(True)

#%%
path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones/Experimento LED/Medicion i vs i 0-20mA fina/res/1 (res).txt'
path2 = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led PID/0-188mA, step 1mA, wait 10ms/res/1 (res).txt'
data2 = np.loadtxt(path2, skiprows=1)
R = data2[:, 1]
N = data2[:, 0]

R_err = error_R(R, 0.000097)

T = [(i - 1000)/3.815 for i in R]
T_err = [i / 3.815 for i in R_err]

plt.figure(3)
#plt.errorbar(N, T, yerr = T_err, fmt = 'k.', capsize = 3)
plt.plot(N, T, 'k.')
#plt.plot(N, [T[i] + T_err[i] for i in range(len(T))], 'r-')
#plt.plot(N, [T[i] - T_err[i] for i in range(len(T))], 'r-')
plt.ylabel('Temperatura (C)', size = 15)
plt.xlabel('Numero de medicion', size = 14)
#plt.axvline(N[int(len(N)/2)], lw = 4)
plt.grid(True)
#%%
############# I_SiPM vs I_LED  de 0 A a 0.188 A con control de temperatura ####################
data = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led PID/0-188mA, step 1mA, wait 10ms/iv/1 (iv).txt')
I_sipm = data[:, 0]
I_led = data[:, 2]
V_led = data[:, 1]

data2 = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led PID/0-188mA, step 1mA, wait 10ms/res/1 (res).txt', skiprows=1)
R = data2[:, 1]
N = data2[:, 0]
T = [(i - 1000)/3.815 for i in R]

plt.figure(3)
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

ax1.plot(I_led, I_sipm, '.')
ax1.set_xlabel(r'$I_{led}$ (A)', size = 15)
ax1.set_ylabel(r'$I_{sipm}$ (A)', size = 15)
ax2.plot(N, T, '.')
ax2.set_ylabel('Temperatura (C)', size = 15)

plt.tight_layout()

#%%
path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones/Experimento LED/Medicion i vs i 0-20mA fina/iv/1 (iv).txt'
data3 = np.loadtxt(path)
I_sipm = data3[:, 0]
I_led = data3[:, 2]

I_led_err = error_I(I_led, '2612', source = True)
I_sipm_err = error_I(I_sipm, '2400', source = False)


plt.figure(4)
plt.plot(I_led, I_sipm, '.')
plt.errorbar(I_led, I_sipm, xerr= I_led_err, yerr = I_sipm_err, fmt = 'none', capsize = 3)
plt.xlabel(r'$I_{led}$ (A)', size = 15)
plt.ylabel(r'$I_{sipm}$ (A)', size = 15)
plt.yscale('log')
plt.xscale('log')
