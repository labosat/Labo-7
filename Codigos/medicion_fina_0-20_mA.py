import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from scipy import integrate
#%%

data = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/hist_vs_wait_time(0-200)/0.01/iv/1 (iv).txt')
I_led = data[:, 2]
I_sipm = data[:, 0]
I_led_err = f.error_I(I_led, '2612', source = True)
I_sipm_err = f.error_I(I_sipm, '2400', source = False)

R = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/hist_vs_wait_time(0-200)/0.01/res/1 (res).txt', skiprows=1)[:, 1]

plt.figure(1)
plt.plot(np.arange(len(R)), R, '--')

plt.figure(2)
plt.plot(I_led, I_sipm, '.')
plt.errorbar(I_led, I_sipm, xerr=I_led_err, yerr=I_sipm_err, fmt = 'k.', capsize = 2)


I_sipm_temp_1 = I_sipm[1:int(len(I_sipm)/2)]
I_led_temp_1 = I_led[1:int(len(I_led)/2)]
I_sipm_temp_2 = I_sipm[int(len(I_sipm)/2)+1:]
I_led_temp_2 = I_led[int(len(I_led)/2)+1:]
area1 = integrate.simps(I_sipm_temp_1, I_led_temp_1) - integrate.simps(I_sipm_temp_2, I_led_temp_2)  

#%%

data = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led PID/0-188mA, step 1mA, wait 10ms/iv/1 (iv).txt')

I_led = data[:, 2]
I_sipm = data[:, 0]
I_led_err = error_I(I_led, '2612', source = True)
I_sipm_err = error_I(I_sipm, '2400', source = False)

R = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led PID/0-188mA, step 1mA, wait 10ms/res/1 (res).txt', skiprows=1)[:, 1]

T = [(i-1000)/3.815 for i in R]

plt.figure(1)
plt.plot(np.arange(len(T)), T, '.')

plt.figure(2)
plt.plot(I_led, I_sipm, '.')
plt.errorbar(I_led, I_sipm, xerr=I_led_err, yerr=I_sipm_err, fmt = 'k.', capsize = 2)


I_sipm_temp_1 = I_sipm[1:int(len(I_sipm)/2)]
I_led_temp_1 = I_led[1:int(len(I_led)/2)]
I_sipm_temp_2 = I_sipm[int(len(I_sipm)/2)+1:]
I_led_temp_2 = I_led[int(len(I_led)/2)+1:]
area2 = integrate.simps(I_sipm_temp_1, I_led_temp_1) - integrate.simps(I_sipm_temp_2, I_led_temp_2)  
