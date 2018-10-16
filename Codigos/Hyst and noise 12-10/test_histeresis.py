#%% code to check hysteresis area with any two methods

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def integrate_simpson(V, I):
    accumulator = ((V[len(V) - 1] - V[0])/len(V))*(I[0]/2 + I[len(I) - 1]/2)
        
    for k in range(1, len(V) - 1):
        accumulator += ((V[len(V) - 1] - V[0])/len(V))*I[k]
        
    return accumulator

def integrate_trapezoid(V, I):
    return (V[len(V) - 1] - V[0])*(I[len(I) - 1] - I[0])/2


folders = 7
current_lib = [0.001, 0.005, 0.01, 0.015, 0.02, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175]

T = []
for i in range(1, folders + 1):
    #windows
    path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i
    
    #linux
    #path = '/home/lucas/Desktop/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i
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

        V_up = []
        V_down = []
        I_down = []
        I_up = []
        
        
        for k in range(0, int(len(I)/2)):
            V_up.append(V[k])
            I_up.append(I[k])
            
        for k in range(int(len(I)/2), len(I)):
            V_down.append(V[k])
            I_down.append(I[k])
            
        area = integrate_simpson(V_up, I_up) - integrate_simpson(V_down, I_down)
        hyst.append(area)
        
        t += (np.mean(R) - 1000)/3.815
            
    T.append(round(t/len(current_lib), 1))
    #plt.figure(i)        
    plt.plot(iled, hyst)
  

plt.xlabel('Led Current [A]')
plt.ylabel('Hysteresis Area [W]')
plt.legend([str(T[0]) + " ºC", str(T[1]) + " ºC", str(T[2]) + " ºC", str(T[3]) + " ºC", str(T[4]) + " ºC", str(T[5]) + " ºC", str(T[6]) + " ºC"])
plt.grid(True)

#%% code to check hysteresis area integrating 7th deg polynomial fit
import numpy as np
import scipy.integrate as integrate

def poly(x, v):
    function = 0
    for i in range(0, len(v)):
        function += v[len(v) - 1 - i]*pow(x, i)
    return function

folders = 7
current_lib = [0.001, 0.005, 0.01, 0.015, 0.02, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175]

T = []
for i in range(1, folders + 1):
    #windows
    path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i
    
    #linux
    #path = '/home/lucas/Desktop/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i
    hyst = []
    hyst_error = []
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
        V_err = V*0.0002 + 5E-3
        I_err = I*0.0002 + 2.5E-6

        V_up = []
        V_down = []
        I_down = []
        I_down_err = []
        I_up = []
        I_up_err = []
        
        
        for k in range(0, int(len(I)/2)):
            V_up.append(V[k])
            I_up.append(I[k])
            I_up_err.append(I_err[k])

            
        for k in range(int(len(I)/2), len(I)):
            V_down.append(V[k])
            I_down.append(I[k])
            I_down_err.append(I_err[k])
            
        fit_up = np.polyfit(V_up, I_up, 9, w=I_up_err)
        fit_down = np.polyfit(V_down, I_down, 9, w=I_down_err)
        
        Int_up = integrate.quad(poly, 23, 30, args=(fit_up))
        Int_down = integrate.quad(poly, 23, 30, args=(fit_down))
        
        #Int_up = integrate_simpson(V_up, I_up)
        #Int_down = integrate_simpson(V_down, I_down)

        area = Int_up[0] - Int_down[0]
        #area = Int_up - Int_down
        
        d_area = abs(Int_up[1]) + abs(Int_down[1])
        hyst.append(area)
        hyst_error.append(d_area)
        
        t += (np.mean(R) - 1000)/3.815
            
    T.append(round(t/len(current_lib), 1))

    plt.grid(True)
    plt.errorbar(iled, hyst, yerr=hyst_error)
    #plt.plot(iled, hyst)
  

plt.xlabel('Led Current [A]')
plt.ylabel('Hysteresis Area [W]')
plt.legend([str(T[0]) + " ºC", str(T[1]) + " ºC", str(T[2]) + " ºC", str(T[3]) + " ºC", str(T[4]) + " ºC", str(T[5]) + " ºC", str(T[6]) + " ºC"])
plt.grid(True)
    
#%% hysteresis distances for different T (fixed current) (not working)

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


folders = 7
current = 0.15


T = []
for i in range(1, folders + 1):
    #windows
    path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i
    
    #linux
    #path = '/home/lucas/Desktop/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i

    hyst_dist = []
    path_file_i = str(current) + 'A/iv/1 (iv).txt'
    path_file_r = str(current) + 'A/res/1 (res).txt'
    data_i = np.loadtxt(path + path_file_i)
    data_r = np.loadtxt(path + path_file_r, skiprows=1)
        
    V = data_i[:, 1]
    I = data_i[:, 2]
    R = data_r[:, 1]

    V_up = []
    V_down = []
    I_down = []
    I_up = []
    
    for k in range(0, int(len(I)/2)):
        V_up.append(V[k])
        I_up.append(I[k])
        
    for k in range(int(len(I)/2), len(I)):
        V_down.append(V[k])
        I_down.append(I[k])
        
    for k in range(0, len(I_up)):
        if len(I_up) == len(I_down):
            hyst_dist.append(I_up[k] - I_down[k])
        else:
            print("I_up and I_down are not the same size")
        
    
    t = round((np.mean(R) - 1000)/3.815)
            
    T.append(t)
    #plt.figure(i)      

    plt.plot(V_up, hyst_dist)
  

plt.xlabel('Led Current [A]')
plt.ylabel('Hysteresis Area [W]')
plt.legend([str(T[0]) + " ºC", str(T[1]) + " ºC", str(T[2]) + " ºC", str(T[3]) + " ºC", str(T[4]) + " ºC", str(T[5]) + " ºC", str(T[6]) + " ºC"])
plt.grid(True)

#%% graphs all iv curves for a given T
import numpy as np
import matplotlib.pyplot as plt

current_lib = [0.001, 0.005, 0.01, 0.015, 0.02, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175]

i = 7

#casa
#path = '/home/lucas/Desktop/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i
        
#labo windows

path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i



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


#%% code to check noise (not working yet. Check measurements)
            
import numpy as np
import matplotlib.pyplot as plt

folders = 6
current_lib = [0.001, 0.005, 0.01, 0.015, 0.02]
NPLC_lib = [0.01, 0.1, 1]

for i in range(0, len(NPLC_lib)):
    
    #this ensures NPLC = 1
    i = 0
    
    plt.figure(i)
    
    for j in range(1, folders + 1):
        #windows
        path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led ruido/Estacionario %s/' % j
        
        #linux
        #path = '/home/lucas/Desktop/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led ruido/Estacionario %s/' % j

        path += str(NPLC_lib[i]) + " NPLC/"
        
        I_led = []
        noise = []
        noise_err = []
        N = []
        
        for k in range(0, len(current_lib)):
            path_i = path + str(current_lib[k]) + "A/iv/1 (iv).txt"
            path_r = path + str(current_lib[k]) + "A/res/1 (res).txt"
            
            data_i = np.loadtxt(path_i, skiprows=1)
            data_r = np.loadtxt(path_r, skiprows=1)
        
            N = []
            I_sipm = data_i[:, 1]
            I_led.append(current_lib[k])
            
            for l in range(0, len(I_sipm)):
                N.append(l)
            
            noise_value = np.sum((np.polyval(np.polyfit(N, I_sipm, 8), N) - I_sipm)**2)

            noise.append(noise_value)
            noise_err.append(np.sqrt(2*pow(noise_value, 4)))
            
        plt.grid(True)
        plt.errorbar(I_led, noise, yerr=noise_err)
        #plt.legend("%s NPLC" % NPLC_lib[i])
            
    break

#plt.plot(N, I_sipm,'.')
#fit = np.polyfit(N, I_sipm, 8)
#plt.plot(N, np.polyval(fit, N))
    
#%% codigo para graficar I_sipm(I_led 0, 20) para distintas T
import numpy as np
import matplotlib.pyplot as plt    

folders = 7
T = []
for i in range(1, folders + 1):
    j = 1
    t = 0
    while j == 1:
        try:
            path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/i_vs_i/Estacionario %s/iv/%s (iv).txt' % (i, j)
            path_r = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/i_vs_i/Estacionario %s/res/%s (res).txt' % (i, j)
    
            data = np.loadtxt(path)
            data_r = np.loadtxt(path_r, skiprows=1)
            R = data_r[:, 1]
            I_led = data[1:199, 2]
            I_sipm = data[1:199, 0]
            
            I_led_err = [x*0.0002 + 2.5E-6 for x in I_led]
            I_sipm_err = [x*0.0025 + 6E-9 for x in I_sipm]
    
            t += round((np.mean(R) - 1000)/3.815, 2)
            
            j += 1
        except IOError:
            break
        
    T.append(t)
    index = len(I_led) - 1
    np.delete(I_led, [index])
    np.delete(I_sipm, [index])

    plt.errorbar(I_led, I_sipm, xerr=I_led_err, yerr=I_sipm_err, fmt='.', capsize=5)
    plt.xlabel('Led Current [A]')
    plt.ylabel('SiPM Current [A]')
    #casa
    #path = '/home/lucas/Desktop/Labo-7/Mediciones/Experimento LED/i_vs_i/Estacionario %s/iv/1 (iv).txt' % i
    #path_r = '/home/lucas/Desktop/Labo-7/Mediciones/Experimento LED/i_vs_i/Estacionario %s/res/1 (res).txt' % i


    #labo windows
    
    
plt.xlabel('Led Current [A]')
plt.ylabel('SiPM Current [A]')
#plt.yscale('log')
#plt.xscale('log')
plt.legend([str(T[0]) + " C", str(T[1]) + " C", str(T[2]) + " C", str(T[3]) + " C", str(T[4]) + " C", str(T[5]) + " C", str(T[6]) + " C"])
plt.grid(True)


#%% codigo para graficar I_sipm(I_led 0, 200) para distintas T
import numpy as np
import matplotlib.pyplot as plt    

folders = 7
T = []
for i in range(1, folders + 1):
    j = 1
    t = 0
    while j == 1:
        try:
            path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/i_vs_i(200)/Estacionario %s/iv/%s (iv).txt' % (i, j)
            path_r = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/i_vs_i(200)/Estacionario %s/res/%s (res).txt' % (i, j)
    
            data = np.loadtxt(path)
            data_r = np.loadtxt(path_r, skiprows=1)
            R = data_r[:, 1]
            I_led = data[1:199, 2]
            I_sipm = data[1:199, 0]
            
            I_led_err = [x*0.0002 + 2.5E-6 for x in I_led]
            I_sipm_err = [x*0.0025 + 6E-9 for x in I_sipm]
    
            t += round((np.mean(R) - 1000)/3.815, 2)
            
            j += 1
        except IOError:
            break
        
    T.append(t)
    index = len(I_led) - 1
    np.delete(I_led, [index])
    np.delete(I_sipm, [index])

    plt.errorbar(I_led, I_sipm, xerr=I_led_err, yerr=I_sipm_err, fmt='.', capsize=5)
    plt.xlabel('Led Current [A]')
    plt.ylabel('SiPM Current [A]')
    #casa
    #path = '/home/lucas/Desktop/Labo-7/Mediciones/Experimento LED/i_vs_i/Estacionario %s/iv/1 (iv).txt' % i
    #path_r = '/home/lucas/Desktop/Labo-7/Mediciones/Experimento LED/i_vs_i/Estacionario %s/res/1 (res).txt' % i


    #labo windows
    
    
plt.xlabel('Led Current [A]')
plt.ylabel('SiPM Current [A]')
#plt.yscale('log')
#plt.xscale('log')
plt.legend([str(T[0]) + " C", str(T[1]) + " C", str(T[2]) + " C", str(T[3]) + " C", str(T[4]) + " C", str(T[5]) + " C", str(T[6]) + " C"])
plt.grid(True)

#%% codigo para ver histeresis en isipm(iled) de 0 a 200 mA

import numpy as np
import scipy.integrate as integrate

def poly(x, v):
    function = 0
    for i in range(0, len(v)):
        function += v[len(v) - 1 - i]*pow(x, i)
    return function

folders = 9
T = []
hyst = []
hyst_error = []
for i in range(1, folders + 1):
    #windows
    path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Experimento LED/i_vs_i(200)/Estacionario %s/' % i
    
    #linux
    #path = '/home/lucas/Desktop/Labo-7/Codigos/Codigos Estabilidad LED-SiPM/results led histeresis/Estacionario %s/' % i
    t = 0

    path_file_i = 'iv/1 (iv).txt'
    path_file_r ='res/1 (res).txt'
    data_i = np.loadtxt(path + path_file_i)
    data_r = np.loadtxt(path + path_file_r, skiprows=1)
    
    Isipm = data_i[1:199, 1]
    Iled = data_i[1:199, 2]
    R = data_r[:, 1]
    Iled_err = Iled*0.0002 + 2.5E-6
    Isipm_err = Isipm*0.00025 + 6E-9

    Isipm_up = []
    Isipm_down = []
    Iled_up = []
    Iled_down = []
    
    Isipm_down_err = []
    Isipm_up_err = []
    
    
    for k in range(0, int(len(Isipm)/2)):
        Isipm_up.append(Isipm[k])
        Iled_up.append(Iled[k])
        Isipm_up_err.append(Isipm_err[k])

        
    for k in range(int(len(Isipm)/2), len(Isipm)):
        Isipm_down.append(Isipm[k])
        Iled_down.append(Iled[k])
        Isipm_down_err.append(Isipm_err[k])
        
    fit_up = np.polyfit(Iled_up, Isipm_up, 9, w=Isipm_up_err)
    fit_down = np.polyfit(Iled_down, Isipm_down, 9, w=Isipm_down_err)
    
    Int_up = integrate.quad(poly, 0, 0.175, args=(fit_up))
    Int_down = integrate.quad(poly, 0, 0.175, args=(fit_down))
    
    #Int_up = integrate_simpson(V_up, I_up)
    #Int_down = integrate_simpson(V_down, I_down)

    area = Int_up[0] - Int_down[0]
    #area = Int_up - Int_down
    
    d_area = abs(Int_up[1]) + abs(Int_down[1])
    hyst.append(area)
    hyst_error.append(d_area)
    
    t += (np.mean(R) - 1000)/3.815
            
    T.append(round(t))

plt.grid(True)
plt.errorbar(T, hyst, yerr=hyst_error)
  

plt.xlabel('Temperature [C]')
plt.ylabel('Hysteresis Area [W]')
plt.grid(True)