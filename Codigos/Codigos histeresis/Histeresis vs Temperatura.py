import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from scipy import integrate

def simps_error(x, x_err, y_1, y_2, y_1_err, y_2_err):
    area = []
    for i in range(10000):
        y_1_temp = [np.random.normal(loc = y_1[j], scale = y_1_err[j]) for j in range(len(y_1))]
        x_temp = [np.random.normal(loc = x[j], scale = x_err[j]) for j in range(len(x))]
        y_2_temp = [np.random.normal(loc = y_2[j], scale = y_2_err[j]) for j in range(len(y_2))]
        
        area.append(integrate.simps(y = y_2_temp, x = x_temp) - integrate.simps(y = y_1_temp, x = x_temp))
    
    return np.std(area)


#%%
R = []
R_err = []
area = []
area_err = []

condition_1 = True
i = 1
while i <= 7:
    area_temp = []
    area_err_temp = []
    R_temp = []
    R_err_temp = []
    condition_2 = True
    j = 1
    while condition_2:
        try:
            Res = np.loadtxt('C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/results led 0-20/Estacionario %s/res/%s (res).txt' % (i, j), skiprows=1)[:, 1]
            R_temp.append(np.mean(Res))
            R_err_temp.append(np.std(Res))
            data_i = np.loadtxt('C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/results led 0-20/Estacionario %s/iv/%s (iv).txt' % (i, j))
            I_sipm = data_i[:, 0]
            I_sipm_1 = I_sipm[1:int(len(I_sipm)/2)]
            I_sipm_2 = np.flip(I_sipm[int(len(I_sipm)/2):-1], axis=0)
            I_sipm_1_err = f.error_I(I_sipm[1:int(len(I_sipm)/2)], '2400', source=False)
            I_sipm_2_err = f.error_I(np.flip(I_sipm[int(len(I_sipm)/2):-1], axis=0), '2400', source=False)
            I_led = data_i[1:int(len(data_i[:, 2])/2), 2]
            I_led_err = f.error_I(I_led, '2612', source=True)
            
            j += 1
            area_temp.append(integrate.simps(y = I_sipm_2, x = I_led) - integrate.simps(y = I_sipm_1, x = I_led))
            area_err_temp.append(simps_error(I_led, I_led_err, I_sipm_1, I_sipm_2, I_sipm_1_err, I_sipm_2_err))
        except IOError:
            condition_2 = False
    area.append(np.mean(area_temp))
    area_err.append(np.linalg.norm(area_err_temp)/np.sqrt(len(area_err_temp)))
    R.append(np.mean(R_temp))
    R_err.append(np.linalg.norm(R_err_temp)/np.sqrt(len(R_err_temp)))
    i += 1

R_err = f.error_R(R, 0.000097)

T = [(m - 1000)/3.815 for m in R]
T_err = [m/3.815 for m in R_err]

area_mA = [100000000 * i for i in area]
area_err_mA = [100000000 * i for i in area_err]
plt.errorbar(T, area_mA, xerr=T_err, yerr=area_err_mA, fmt = 'ok', capsize = 3)
plt.ylabel(r'Histeresis Area  ($\mu A^2$)', size=22)
plt.xlabel('Temperatura (C)', size = 22)
plt.tick_params(labelsize=22)
plt.grid(True)

#%%
plt.loglog(data_i[1:-1, 2], data_i[1:-1, 0], '.')
plt.ylabel(r'$I_{SiPM}$', size=22)
plt.xlabel(r'$I_{led}$', size = 22)
plt.tick_params(labelsize=22)
plt.grid(True)