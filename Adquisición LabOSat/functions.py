from __future__ import division
#import visa
import time
import matplotlib.pyplot as plt
import os
import numpy as np


def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]


def gpib(address1, address2):

    rm = visa.ResourceManager()
    equipment_id1 = 'GPIB0::' + str(address1) + '::INSTR'
    equipment_id2 = 'GPIB0::' + str(address2) + '::INSTR'
    
    smu_2612b = rm.open_resource(equipment_id1)
    smu_2400 = rm.open_resource(equipment_id2)

    print("Installed equipment:")
    
    smu_2612b.write('smua.reset()')
    smu_2612b.write('smub.reset()')
    
    print(smu_2612b.query("*IDN?"))
    print(smu_2400.query("*IDN?"))
       
    smu_2612b.write('reset()')
    smu_2400.write("*RST")
    
    return smu_2612b, smu_2400, rm


#could pur a flag on plot to decide what data to plot (I, V, R)
def plot(x, y, char1, char2, n, log=False, errorbars_2400=False, errorbars_2612=False):
    graph = plt.figure(n)
    #plt.hold(True)
    
    if errorbars_2612:
        y_err = error_I(y, '2612', source=False)
        x_err = error_I(x, '2612', source=True)
        plt.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='.k', capsize=3)
        
    if errorbars_2400:
        y_err = [0.0007*i + 0.3 for i in y]
        plt.errorbar(x, y, yerr=y_err, fmt='.k', capsize=3)

    else:
        plt.plot(x, y, '.', linewidth = 1.0)
        #plt.legend(loc = 'best')

    if (char1 == 'N'):
        plt.xlabel('Number of measurement', fontsize = 14)
    if (char1 == 't'):
        plt.xlabel('Time [s]', fontsize = 14)
    elif (char1 == 'V'):
        plt.xlabel('Voltage [V]', fontsize = 14)
    elif (char1 == 'I'):
        plt.xlabel('Current [A]', fontsize = 14) 
    elif (char1 == 'Vled'):
        plt.xlabel('Led Voltage [V]', fontsize = 14)
    elif (char1 == 'Iled'):
        plt.xlabel('Led Current [A]', fontsize = 14)
    elif (char1 == 'Powled'):
        plt.xlabel('Led Power [W]', fontsize = 14)
    
    if (char2 == 'R'):
        plt.ylabel('Resistance [Ohm]', fontsize = 14)
    elif (char2 == 'I'):
        plt.ylabel('Current [A]', fontsize = 14)
    elif (char2 == 'Isipm'):
        plt.ylabel('SiPM Current [A]', fontsize = 14)
        
    if log:
        plt.xscale('log')
        plt.yscale('log')
    plt.grid(True)
    plt.tight_layout(True)
    
    plt.show()
    return graph


def save(readingsV_sipm, readingsI_sipm, readingsV_led, readingsI_led, 
            readingsR, graphIV, graphR, number, group_path):
    
    #[unused,unused,dateString] = date_time_now()
    # For makin this cross platform, change the path name
    path            = ".\\results\\" + group_path + "\\"
    path_fig        = ".\\results\\" + group_path + "\\figures\\"
    ext_fig         = ".png" 
    ext_txt         = ".txt" 
    figure_nameIV   = path_fig + str(number) + " (iv)" + ext_fig
    figure_nameR    = path_fig + str(number) + " (res)" + ext_fig
    text_name       = path + str(number) + ext_txt
    
    """
    Check if the folder exists. This is only Windows compatible (because of VISA)
    """
        
    if not(os.path.exists(path)):
        os.makedirs(path)
        
    if not(os.path.exists(path_fig)):
        os.makedirs(path_fig)
          
    File = open(text_name, 'w')
    
    File.write("V_sipm\tI_sipm\tV_led\tI_led\tR_rtd\n")
    #format is I_sipm, V_led, I_led
    if len(readingsI_sipm) == len(readingsI_led) and len(readingsI_sipm) == len(readingsR): 
        for i in range(0,len(readingsI_sipm)):
            line = str(readingsV_sipm[i]) + '\t' + str(readingsI_sipm[i]) + '\t' + str(readingsV_led[i]) + '\t' + str(readingsI_led[i]) + '\t' + str(readingsR[i]) + '\n' 
            File.write(line)
            

    File.close()
    if graphIV != 'NULL':
        graphIV.savefig(figure_nameIV, dpi=250, bbox_inches='tight')
    if graphR != 'NULL':
        graphR.savefig(figure_nameR, dpi=250, bbox_inches='tight')
        

def save_iv(readingsV_sipm, readingsI_sipm, 
            readingsR, graphIV, graphR, number, group_path):
    
    #[unused,unused,dateString] = date_time_now()
    # For makin this cross platform, change the path name
    path            = ".\\results\\" + group_path + "\\"
    path_fig        = ".\\results\\" + group_path + "\\figures\\"
    ext_fig         = ".png" 
    ext_txt         = ".txt" 
    figure_nameIV   = path_fig + str(number) + " (iv)" + ext_fig
    figure_nameR    = path_fig + str(number) + " (res)" + ext_fig
    text_name       = path + str(number) + ext_txt
    
    """
    Check if the folder exists. This is only Windows compatible (because of VISA)
    """
        
    if not(os.path.exists(path)):
        os.makedirs(path)
        
    if not(os.path.exists(path_fig)):
        os.makedirs(path_fig)
          
    File = open(text_name, 'w')
    
    File.write("V_sipm\tI_sipm\tR_rtd\n")
    #format is I_sipm, V_led, I_led
    if len(readingsI_sipm) == len(readingsV_sipm):
        for i in range(0,len(readingsI_sipm)):
            line = str(readingsV_sipm[i]) + '\t' + str(readingsI_sipm[i]) + '\t' + str(readingsR[i]) + '\n' 
            File.write(line)
            

    File.close()
    if graphIV != 'NULL':
        graphIV.savefig(figure_nameIV, dpi=250, bbox_inches='tight')
    if graphR != 'NULL':
        graphR.savefig(figure_nameR, dpi=250, bbox_inches='tight')
        

def save_dark(readingsI_sipm, readingsR, graphR, number, group_path):
    
    #[unused,unused,dateString] = date_time_now()
    # For makin this cross platform, change the path name
    
    path            = ".\\results\\" + group_path + "\\"
    path_fig        = ".\\results\\" + group_path + "\\figures\\"
    ext_fig         = ".png" 
    ext_txt         = ".txt" 
    text_name       = path + str(number) + ext_txt
    figure_nameR    = path_fig + str(number) + " (res)" + ext_fig
    
    """
    Check if the folder exists. This is only Windows compatible (because of VISA)
    """
        
    if not(os.path.exists(path)):
        os.makedirs(path)
        
    if not(os.path.exists(path_fig)):
        os.makedirs(path_fig)
          
    File = open(text_name, 'w')
    
    File.write("I_sipm\tR_rtd\n")
    #format is I_sipm, V_led, I_led
    if len(readingsI_sipm) == len(readingsR):
        for i in range(0,len(readingsI_sipm)):
            line = str(readingsI_sipm[i]) + '\t' + str(readingsR[i]) + '\n' 
            File.write(line)
            

    File.close()
    if graphR != 'NULL':
        graphR.savefig(figure_nameR, dpi=250, bbox_inches='tight')
    return


def P(prefix):
    if prefix == 'p':
        return 1E-12
    if prefix == 'n':
        return 1E-09
    if prefix == 'u':
        return 1E-06    
    if prefix == 'm':
        return 1E-03
    if prefix == 'k':
        return 1E+03
    if prefix == 'M':
        return 1E+06
    if prefix == 'G':
        return 1E+09


"""----------------------------------------------------------------------------
Configuration functions for 2612B
----------------------------------------------------------------------------"""

def readBuffer(smu, char):
    
    if (char == 'a'):
        measure    = smu.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.readings)')
        source     = smu.query('printbuffer(1, smua.nvbuffer1.n, smua.nvbuffer1.sourcevalues)')
    if (char == 'b'):
        measure    = smu.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.readings)')
        source     = smu.query('printbuffer(1, smub.nvbuffer1.n, smub.nvbuffer1.sourcevalues)')
    
    return measure, source  

def cast(string):
   out = []
   for values in string.split(','):
       aux = values
       out.append(float(aux))
   return out

def split(v, i, r):
    v_pos = []
    v_neg = []
    i_pos = []
    i_neg = []
    r_pos = []
    r_neg = []
    
    for j in range(len(v)):
        if v[j] <= 0:
            v_neg.append(v[j])
            i_neg.append(i[j])
            r_neg.append(r[j])
        elif v[j] >= 0:
            v_pos.append(v[j])
            i_pos.append(i[j])
            r_pos.append(r[j])
            
    v_neg = v_neg[::-1]
    v_neg = [-g for g in v_neg]
    i_neg = i_neg[::-1]
    i_neg = [-g for g in i_neg]
    r_neg = r_neg[::-1]
    
    return v_neg, v_pos, i_neg, i_pos, r_neg, r_pos

def Thermostat(smu, R_condition, condition, tolerance, i):
    if R_condition > (condition + tolerance):
        smu.write('smub.level.i = 0')
        time.sleep(30)
    elif R_condition < (condition - tolerance):
        smu.write('smub.level.i = 0.002')
        time.sleep(5)
    
    smu.write('smub.level.i = ' + str(i))
    return
    
def ThermostatInitial(smu, tolerance):
    import numpy as np
    import time
       
    condition = True
    readingsRLimit = []
    
    smu.write('OUTP ON')
    while condition:
        readingsRLimit = []
        step = 0 
        while (step <= 150):
            auxRead = smu.query(':READ?')
            rtd_r = float(cast(auxRead)[2])
            readingsRLimit.append(rtd_r)
            step += 1 
        time.sleep(10)
        
        if np.std(readingsRLimit) <= tolerance:
            condition = False
            time.sleep(2)
    

    smu.write('OUTP OFF')    
    return np.mean(readingsRLimit)



def error_I(y, SMU, source = False):
    """
    Esta funcion esta diseniada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonc
    I_led_temp_1 = I_led[1:int(len(I_led)/2)]es la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    if SMU == '2612':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.0003
                    offset = 800*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.0003
                    offset = 5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0003
                    offset = 60*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0003
                    offset = 300*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0003
                    offset = 6*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0003
                    offset = 30*pow(10, -6)                
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0005
                    offset = 1.8*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <= 1.5: 
                    percentage = 0.0006
                    offset = 4*pow(10, -3)
                else:
                    percentage = 0.005
                    offset = 40*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00025
                    offset = 500*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.00025
                    offset = 1.5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0002
                    offset = 25*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0002
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0002
                    offset = 2.5*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0002
                    offset = 20*pow(10, -6)                
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0003
                    offset = 1.5*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <=1.5: 
                    percentage = 0.0005
                    offset = 3.5*pow(10, -3)
                else:
                    percentage = 0.004
                    offset = 25*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00029
                    offset = 300*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00027
                    offset = 700*pow(10, -12)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00025
                    offset = 6*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00027
                    offset = 60*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00035
                    offset = 600*pow(10, -9)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00055
                    offset = 6*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0022
                    offset = 570*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00035
                    offset = 600*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00033
                    offset = 2*pow(10, -9)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00031
                    offset = 20*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00034
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00045
                    offset = 2*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00066
                    offset = 20*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0027
                    offset = 900*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')        
    
    return temp


def error_V(x, SMU, source = True):
    """
    Esta funcion esta diseniada para crear un array con los errores del voltaje 
    medido o sourceado por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene el voltaje, y un boolean que indica si el 
    mismo fue medido o sourceado.
    
    Input: (V, source = True)
    
    Si no se especifica el source, entonces el voltaje fue sourceado. Si source = False,
    entonces se midio voltaje.
    
    Returns:  V_err  (list)
    .
    .
    """
    if SMU == '2612':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 375*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00015
                    offset = 225*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 350*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 600*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 2.4*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 24*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00012
                    offset = 300*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.00012
                    offset = 300*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 1.5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 10*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
        
    return temp    

    
def error_R(x):
	temp = []
	for i in range(len(x)):
		temp.append(x[i]*0.0007 + 0.3)

	return np.asanyarray(temp)

# functions for data analysis -------------------------------------------------

def dispersion(x):
    return np.sqrt(np.sum(((x - np.mean(x))**2)/(len(x)-1)))

def tolerance(tolerance, path):
    """
    Esta funcion itera sobre todos los sets de datos que se encuentren en la carpeta 
    del path, y filtra las N mediciones para quedarme solo con las que tienen
    dispersion <= tolerancia. Me devuelve un array sobre el cual tengo analizar los datos,
    asegurandome de que la dispersion en temperatura fue menor a la deseada.
    No hay que poner el numero de mediciones, python las cuenta solo. 
    Solo hay que poner el path!
    Los archivos a iterar deben estar en una location terminada en '/res/i (res).txt', 
    donde i es el numero de set de datos (de 1 a N).
    Tolerancia tipica para mediciones en temperatura en el estacionario ==> 0.03
    
    Input: (tolerancia, path)
    
    Returns: list
    .
    .
    """
    meas_filter = []
    i = 1
    while True:
        try:
            data = np.loadtxt(path + '/%s.txt' % i, skiprows=1)
            Res = data[:, 2]
            if dispersion(Res) <= tolerance:
                meas_filter.append(i)
            
            i += 1
        except IOError:
            break
        
    return meas_filter

def weightedMean(measurements, weights):
    """
    Devuelve el promedio pesado de una muestra con sus respectivos errores.
    
    Input: (X, X_err)  lists
    
    Returns: float
    .
    .
    """
    wTotal = 0
    mwTotal = 0
    mean = 0
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    for i in range(0, len(measurements)):
        mwTotal += measurements[i]*(1/weights[i]**2)
    mean = mwTotal / wTotal 
    return mean

def Linear(M, x):
    m, b = M
    return m*x + b
    
    
def ClosestToOne(v):
    """
    Esta funcion toma una lista, y devuelve el indice del elemento mas cercano a 1 de 
    la lista.
    
    Input: list
    
    Returns: int  (index)
    .
    .
    """
    compliance = []
    for j in range(0, len(v)):
        compliance.append(abs(v[j] - 1))
    return compliance.index(np.min(compliance))

