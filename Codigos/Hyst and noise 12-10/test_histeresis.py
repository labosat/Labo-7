#%% code to check hysteresis

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

folders = 7
current_lib = [0.001, 0.005, 0.01, 0.015, 0.02, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175]

T = []
for i in range(1, folders + 1):
    #windows
    #path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led/Estacionario %s/' % i
    
    #linux
    path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led/Estacionario %s/' % i
    hyst = []
    iled = []
    t = 0
    
    for j in range(0, len(current_lib)):
        path_file_i = str(current_lib[j]) + 'A/iv/1 (iv).txt'
        path_file_r = str(current_lib[j]) + 'A/res/1 (res).txt'
        data_i = np.loadtxt(path + path_file_i)
        data_r = np.loadtxt(path + path_file_r, skiprows=1)
        
        iled.append(current_lib[j])
        
        V = data_i[:, 1]
        I = data_i[:, 2]
        R = data_r[:, 1]

        I_down = []
        I_up = []
        
        #hysteresis test per point
        hyst_distance = []
        
        for k in range(0, int(len(I)/2)):
            I_up.append(I[k])
            
        for k in range(int(len(I)/2), len(I)):
            I_down.append(I[k])
            
        for k in range(0, len(I_up)):
            if len(I_up) == len(I_down):
                hyst_distance.append(abs(I_up[k] - I_down[k]))
            else:
                print("I_up and I_down are not the same size")
            
        max_hyst = np.max(hyst_distance)
        hyst.append(max_hyst)
        
        t += (np.mean(R) - 1000)/3.815
            
    T.append(round(t/len(current_lib), 1))
    #plt.figure(i)        
    plt.plot(iled, hyst)
  

plt.xlabel('Led Current [A]')
plt.ylabel('Maximum Hysteresis [A]')
plt.legend([str(T[0]), str(T[1]), str(T[2]), str(T[3]), str(T[4]), str(T[5]), str(T[6])])
plt.grid(True)
    
#%% graphs all iv curves for a given T
import numpy as np
import matplotlib.pyplot as plt

current_lib = [0.001, 0.005, 0.01, 0.015, 0.02, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175]

i = 7

path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led/Estacionario %s/' % i
    
for j in range(0, len(current_lib)):
    path_file_i = str(current_lib[j]) + 'A/iv/1 (iv).txt'
    data_i = np.loadtxt(path + path_file_i)
        
    V = data_i[:, 1]
    I = data_i[:, 2]
    V_err = V*0.0002 + 5E-3
    I_err = I*0.0002 + 2.5E-6
    
    plt.errorbar(V, I, xerr=V_err, yerr=I_err, fmt='.')
    
plt.legend(["1 mA", "5 mA", "10 mA", "15 mA", "20 mA", "25 mA", "50 mA", "75 mA", "100 mA", "125 mA", "150 mA", "175 mA"])
plt.xlabel('SiPM Voltage [V]')
plt.ylabel('SiPM Current [A]')
plt.grid(True)
    
#%% code to check noise
            
import numpy as np
import matplotlib.pyplot as plt

folders = 6
current_lib = [0.001, 0.005, 0.01, 0.015, 0.02]
NPLC_lib = [0.01, 0.1, 1]

for i in range(0, len(NPLC_lib)):
    
    #this ensures NPLC = 1
    i = 2
    
    plt.figure(i)
    
    for j in range(1, folders + 1):
        #windows
        #path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led ruido/Estacionario %s/' % j
        
        #linux
        path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led ruido/Estacionario %s/' % j

        path += str(NPLC_lib[i]) + " NPLC/"
        
        I_led = []
        noise = []
        
        for k in range(0, len(current_lib)):
            path_i = path + str(current_lib[k]) + "A/iv/1 (iv).txt"
            path_r = path + str(current_lib[k]) + "A/res/1 (res).txt"
            
            data_i = np.loadtxt(path_i, skiprows=1)
            data_r = np.loadtxt(path_r, skiprows=1)
        
            I_sipm = data_i[:, 1]
            I_led.append(current_lib[k])
            
            noise_value = np.std(I_sipm)
            noise.append(noise_value)
            
        plt.plot(I_led, noise, '.')
        #plt.legend("%s NPLC" % NPLC_lib[i])
            
    break