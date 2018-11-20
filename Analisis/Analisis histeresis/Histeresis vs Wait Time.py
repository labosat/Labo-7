import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from scipy import integrate

def simps_error(x, x_err, y_1, y_1_err, y_2, y_2_err):
    area = []
    for i in range(1000):
        y_1_temp = [np.random.normal(loc = y_1[i], scale = y_1_err[i]) for i in range(len(y_1))]
        x_temp = [np.random.normal(loc = x[i], scale = x_err[i]) for i in range(len(x))]
        y_2_temp = [np.random.normal(loc = y_2[i], scale = y_2_err[i]) for i in range(len(y_2))]
        
        area.append(integrate.simps(y = y_2_temp, x = x_temp) - integrate.simps(y = y_1_temp, x = x_temp))
    
    return np.std(area)
#%%
R = []
R_err = []
area = []
area_err = []
wait_time = [0.01, 0.001, 0.0001,'1e-5', '1e-6', '1e-7']
for i in wait_time:
    area_temp = []
    area_err_temp = []
    R_temp = []
    R_err_temp = []
    Res = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones/Experimento LED/hist_vs_wait_time(0-20)/' + str(i) + '/res/1 (res).txt', skiprows=1)[:, 1]
    R_temp.append(np.mean(Res))
    R_err_temp.append(np.std(Res))
    data_i = np.loadtxt('/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones/Experimento LED/hist_vs_wait_time(0-20)/' + str(i) + '/iv/1 (iv).txt')
    I_sipm = data_i[:, 0]
    I_sipm_1 = I_sipm[1:int(len(I_sipm)/2)+1]
    I_sipm_2 = np.flip(I_sipm[int(len(I_sipm)/2)+1:], axis=0)
    I_sipm_1_err = f.error_I(I_sipm[1:int(len(I_sipm)/2)+1], '2400', source=False)
    I_sipm_2_err = f.error_I(np.flip(I_sipm[int(len(I_sipm)/2)+1:], axis=0), '2400', source=False)
    I_led = data_i[1:int(len(data_i[:, 2])/2)+1, 2]
    I_led_err = f.error_I(I_led, '2612', source=True)

    area_temp.append(integrate.simps(y = I_sipm_2, x = I_led) - integrate.simps(y = I_sipm_1, x = I_led))
    area_err_temp.append(simps_error(I_led_1, I_led_err, I_sipm_1, I_sipm_1_err, I_sipm_2, I_sipm_2_err))

    area.append(np.mean(area_temp))
    area_err.append(np.linalg.norm(area_err_temp)/np.sqrt(len(area_err_temp)))
    R.append(np.mean(R_temp))
    R_err.append(np.linalg.norm(R_err_temp)/np.sqrt(len(R_err_temp)))

R_err = f.error_R(R, 0.000097)

T = [(i - 1000)/3.815 for i in R]
T_err = [i/3.815 for i in R_err]

wait_time = [0.01, 0.001, 0.0001, 1e-5, 1e-6, 1e-7]


area_mA = [100000000 * i for i in area]
area_err_mA = [100000000 * i for i in area_err]

plt.errorbar(wait_time, area_mA, yerr=area_err_mA, fmt = 'ok', capsize = 3)
plt.ylabel(r'Histeresis Area  ($\mu A^2$)', size=17)
plt.xlabel('Wait time (s)', size = 17)
plt.tick_params(labelsize=16)
plt.xscale('log')
plt.grid(True)