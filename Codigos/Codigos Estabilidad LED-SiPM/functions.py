from __future__ import division
import visa
import time
import matplotlib.pyplot as plt
import os


def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]


def gpib(address):

    rm = visa.ResourceManager()
    equipment_id = 'GPIB0::' + str(address) + '::INSTR'
    
    smu = rm.open_resource(equipment_id)

    print("Installed equipment:")
    
    smu.write('smua.reset()')
    smu.write('smub.reset()')
    
    print(smu.query("*IDN?")) 
       
    smu.write('reset()')
    
    return smu, rm

def gpib2(address1, address2):

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

def usb(address, rm):
    equipment_id = 'USB0::' + address + '::INSTR'
    
    DC_supply = rm.open_resource(equipment_id)
    
    print("Installed equipment:")
    
    print(DC_supply.query("*IDN?")) 
    
    return DC_supply

#could pur a flag on plot to decide what data to plot (I, V, R)
def plot(x, y, char1, char2, n):
    graph = plt.figure(n)
    #plt.hold(True)
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
    
    if (char2 == 'R'):
        plt.ylabel('Resistance [Ohm]', fontsize = 14)
    elif (char2 == 'I'):
        plt.ylabel('Current [A]', fontsize = 14)
    elif (char2 == 'Isipm'):
        plt.ylabel('SiPM Current [A]', fontsize = 14)
    plt.grid(True)
    
    plt.show()
    return graph


def save(readingsV, readingsI, readingsR, readingsIR, graphIV, graphR, number, group_path):
    #[unused,unused,dateString] = date_time_now()
    # For makin this cross platform, change the path name
    path            = ".\\results\\" + group_path + "\\"
    path_fig        = ".\\results\\" + group_path + "\\figures\\"
    ext_fig         = ".png" 
    ext_txt         = ".txt" 
    figure_nameIV   = path_fig + str(number) + " (iv)" + ext_fig
    figure_nameR    = path_fig + str(number) + " (res)" + ext_fig
    text_nameIV     = path + "iv\\" + str(number) + " (iv)" + ext_txt
    text_nameR      = path + "res\\" + str(number) + " (res)" + ext_txt
    
    """
    Check if the folder exists. This is only Windows compatible (because of VISA)
    """
        
    if not(os.path.exists(path)):
        os.makedirs(path)
        
    if not(os.path.exists(path_fig)):
        os.makedirs(path_fig)
        
    if not(os.path.exists(path + "iv\\")):
        os.makedirs(path + "iv\\")
        
    if not(os.path.exists(path + "res\\")):
        os.makedirs(path + "res\\")
    
    FileIV = open(text_nameIV, 'w')
    FileR = open(text_nameR, 'w')
    
    #FileIV.write("V\tI\n")
    if len(readingsV) == len(readingsI): 
        for i in range(0,len(readingsV)):
            line = str(readingsV[i]) + '\t' + str(readingsI[i]) + '\n' 
            FileIV.write(line)
            
            
    Number = []
    for i in range(0, len(readingsR)):
        Number.append(i)
    FileR.write("N\tR\tI\n")
    if len(readingsIR) == len(readingsR): 
        for i in range(0,len(readingsR)):
            line = str(Number[i]) + '\t' + str(readingsR[i]) + '\t' + str(readingsIR[i]) + '\n' 
            FileR.write(line)

    FileIV.close()
    FileR.close()
    if graphIV != 'NULL':
        graphIV.savefig(figure_nameIV, dpi=250, bbox_inches='tight')
    if graphR != 'NULL':
        graphR.savefig(figure_nameR, dpi=250, bbox_inches='tight')


def save_led(readingsI_sipm, readingsV_led, readingsI_led, 
             readingsR, readingsIR, graphIV, graphR, number, group_path):
    #[unused,unused,dateString] = date_time_now()
    # For makin this cross platform, change the path name
    path            = ".\\results led\\" + group_path + "\\"
    path_fig        = ".\\results led\\" + group_path + "\\figures\\"
    ext_fig         = ".png" 
    ext_txt         = ".txt" 
    figure_nameIV   = path_fig + str(number) + " (iv)" + ext_fig
    figure_nameR    = path_fig + str(number) + " (res)" + ext_fig
    text_nameIV     = path + "iv\\" + str(number) + " (iv)" + ext_txt
    text_nameR      = path + "res\\" + str(number) + " (res)" + ext_txt
    
    """
    Check if the folder exists. This is only Windows compatible (because of VISA)
    """
        
    if not(os.path.exists(path)):
        os.makedirs(path)
        
    if not(os.path.exists(path_fig)):
        os.makedirs(path_fig)
        
    if not(os.path.exists(path + "iv\\")):
        os.makedirs(path + "iv\\")
        
    if not(os.path.exists(path + "res\\")):
        os.makedirs(path + "res\\")
    
    FileIV = open(text_nameIV, 'w')
    FileR = open(text_nameR, 'w')
    
    #FileIV.write("I_sipm\tV_led\tI_led\n")
    #format is I_sipm, V_led, I_led
    if len(readingsI_sipm) == len(readingsV_led): 
        for i in range(0,len(readingsI_sipm)):
            line = str(readingsI_sipm[i]) + '\t' + str(readingsV_led[i]) + '\t' + str(readingsI_led[i]) + '\n' 
            FileIV.write(line)
            
            
    Number = []
    for i in range(0, len(readingsR)):
        Number.append(i)
    FileR.write("N\tR\tI\n")
    if len(readingsIR) == len(readingsR): 
        for i in range(0,len(readingsR)):
            line = str(Number[i]) + '\t' + str(readingsR[i]) + '\t' + str(readingsIR[i]) + '\n' 
            FileR.write(line)

    FileIV.close()
    FileR.close()
    if graphIV != 'NULL':
        graphIV.savefig(figure_nameIV, dpi=250, bbox_inches='tight')
    if graphR != 'NULL':
        graphR.savefig(figure_nameR, dpi=250, bbox_inches='tight')
        

def save_led2(Time, readingsI_sipm, readingsV_led, readingsR, readingsIR, 
              graphI, graphR, number, group_path):
    #[unused,unused,dateString] = date_time_now()
    # For makin this cross platform, change the path name
    path            = ".\\results led ruido\\" + group_path + "\\"
    path_fig        = ".\\results led ruido\\" + group_path + "\\figures\\"
    ext_fig         = ".png" 
    ext_txt         = ".txt" 
    figure_nameI   = path_fig + str(number) + " (iv)" + ext_fig
    figure_nameR    = path_fig + str(number) + " (res)" + ext_fig
    text_nameI     = path + "iv\\" + str(number) + " (iv)" + ext_txt
    text_nameR      = path + "res\\" + str(number) + " (res)" + ext_txt
    
    """
    Check if the folder exists. This is only Windows compatible (because of VISA)
    """
        
    if not(os.path.exists(path)):
        os.makedirs(path)
        
    if not(os.path.exists(path_fig)):
        os.makedirs(path_fig)
        
    if not(os.path.exists(path + "iv\\")):
        os.makedirs(path + "iv\\")
        
    if not(os.path.exists(path + "res\\")):
        os.makedirs(path + "res\\")
    
    FileIV = open(text_nameI, 'w')
    FileR = open(text_nameR, 'w')
    
    #FileIV.write("I_sipm\tV_led\tI_led\n")
    #format is I_sipm, V_led, I_led
    if len(readingsI_sipm) == len(Time): 
        for i in range(0,len(readingsI_sipm)):
            line = str(Time[i]) + '|t' + str(readingsI_sipm[i]) + '\t' + str(readingsV_led[i]) + '\n' 
            FileIV.write(line)
            
    FileR.write("time\tR\tI\n")
    if len(readingsIR) == len(readingsR): 
        for i in range(0,len(readingsR)):
            line = str(Time[i]) + '\t' + str(readingsR[i]) + '\t' + str(readingsIR[i]) + '\n' 
            FileR.write(line)

    FileIV.close()
    FileR.close()
    if graphI != 'NULL':
        graphI.savefig(figure_nameI, dpi=250, bbox_inches='tight')
    if graphR != 'NULL':
        graphR.savefig(figure_nameR, dpi=250, bbox_inches='tight')


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

