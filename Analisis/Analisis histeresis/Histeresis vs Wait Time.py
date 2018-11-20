import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from scipy import integrate

def simps_error(x, x_err, y_1, y_2, y_1_err, y_2_err):
    area = []
    area_return = []
    for i in range(10):
        y_1_temp = [np.random.normal(loc = y_1[j], scale = y_1_err[j]) for j in range(len(y_1))]
        x_temp = [np.random.normal(loc = x[j], scale = x_err[j]) for j in range(len(x))]
        y_2_temp = [np.random.normal(loc = y_2[j], scale = y_2_err[j]) for j in range(len(y_2))]
        
        area.append(integrate.simps(y = y_2_temp, x = x_temp) - integrate.simps(y = y_1_temp, x = x_temp))
    
    std = np.std(area)
    mean = np.mean(area)
    area_return = [area[i] for i in range(len(area)) if area[i] < mean + std and area[i] > mean - std]
    area_return_2 = [area_return[i] for i in range(len(area_return)) if area_return[i] < mean + std and area_return[i] > mean - std]

    return np.std(area_return_2)
#%%
R = []
R_err = []
area = []
area_err = []
wait_time = ["1e-7", "1e-6", "1e-5", "0.0001", "0.001", "0.01", "0.025", "0.05", "0.075", "0.1", "1"]
for i in wait_time:
    area_temp = []
    area_err_temp = []
    R_temp = []
    R_err_temp = []
    Res = np.loadtxt('C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/Histeresis vs wait time/' + str(i) + '/res/1 (res).txt', skiprows=1)[:, 1]
    R_temp.append(np.mean(Res))
    R_err_temp.append(np.std(Res))
    data_i = np.loadtxt('C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Analisis/Analisis histeresis/Mediciones histeresis/Histeresis vs wait time/' + str(i) + '/iv/1 (iv).txt')
    I_sipm = data_i[1:-1, 0]
    I_sipm_1 = I_sipm[:int(len(I_sipm)/2)]
    I_sipm_2 = np.flip(I_sipm[int(len(I_sipm)/2):], axis=0)
    I_sipm_1_err = f.error_I(I_sipm[:int(len(I_sipm)/2)], '2400', source=False)
    I_sipm_2_err = f.error_I(np.flip(I_sipm[int(len(I_sipm)/2):], axis=0), '2400', source=False)
    I_led = data_i[1:int(len(data_i[:, 2])/2), 2]
    I_led_err = f.error_I(I_led, '2612', source=True)

    area_temp.append(integrate.simps(y = I_sipm_2, x = I_led) - integrate.simps(y = I_sipm_1, x = I_led))
    area_err_temp.append(simps_error(I_led, I_led_err, I_sipm_1, I_sipm_1_err, I_sipm_2, I_sipm_2_err))

    area.append(np.mean(area_temp))
    area_err.append(np.linalg.norm(area_err_temp)/np.sqrt(len(area_err_temp)))
    R.append(np.mean(R_temp))
    R_err.append(np.linalg.norm(R_err_temp)/np.sqrt(len(R_err_temp)))
    
R_err = f.error_R(R, 0.000097)

T = [(i - 1000)/3.815 for i in R]
T_err = [i/3.815 for i in R_err]

wait_time = [1e-7, 1e-6, 1e-5, 0.0001, 0.001, 0.01, 0.025, 0.05, 0.075, 0.1, 1]


area_mA = [100000000 * i for i in area]
area_err_mA = [100000000 * i for i in area_err]

plt.errorbar(wait_time, area_mA, yerr=area_err_mA, fmt = 'sk', capsize = 3)
plt.ylabel(r'Histeresis Area  ($\mu A^2$)', size=22)
plt.xlabel('Wait time (s)', size = 22)
plt.tick_params(labelsize=22)
plt.xscale('log')
plt.grid(True)


#%%

x = np.arange(0, 10, 0.1)
y = 2 * x
x_2 = [np.random.normal(loc=x[i], scale=0.01*x[i]) for i in range(len(x))]
y_2 = [np.random.normal(loc=y[i], scale=0.01*y[i]) for i in range(len(y))]

area = integrate.simps(y=y, x=x)
area_2 = integrate.simps(y=y_2, x=x_2)

area_temp = []
for i in range(100):
    x_2 = [np.random.normal(loc=x[i], scale=0.01*x[i]) for i in range(len(x))]
    y_2 = [np.random.normal(loc=y[i], scale=0.01*y[i]) for i in range(len(y))]
    area_temp.append(integrate.simps(y = y_2, x = x_2))


    
std = np.std(area_temp)
mean = np.mean(area_temp)
area_return = [area_temp[i] for i in range(len(area_temp)) if area_temp[i] < mean + std and area_temp[i] > mean - std]

plt.hist(area_return)