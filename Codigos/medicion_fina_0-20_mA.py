import numpy as np
import matplotlib.pyplot as plt
import Funciones as f

data = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/Medicion i vs i 0-20mA fina/iv/1 (iv).txt')
I_led = data[:, 2]
I_sipm = data[:, 0]
I_led_err = f.error_I(I_led, '2612', source = True)
I_sipm_err = f.error_I(I_sipm, '2400', source = False)

R = np.loadtxt('/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/Medicion i vs i 0-20mA fina/res/1 (res).txt', skiprows=1)[:, 1]

plt.figure(1)
plt.plot(np.arange(len(R)), R, '--')

plt.figure(2)
plt.loglog(I_led, I_sipm, '.')
plt.errorbar(I_led, I_sipm, xerr=I_led_err, yerr=I_sipm_err, fmt = 'k.', capsize = 2)
