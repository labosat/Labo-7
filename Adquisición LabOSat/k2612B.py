from functions import clear_all, gpib, plot, save, save_iv, save_dark, split
from setup import setup
from tests import SelfHeating, IVComplete, DarkCurrent
import time

def run(n, test, group_path, plotFlag, saveFlag):

    # Loading setups configurations
    config = setup()
    
    #rm-list_resources() to find address for smu
    address_2612b = 26
    address_2400 = 24
    
    clear_all()
    
    #running tests (smua measures iv and smub measures r)
    
    [smu_2612b, smu_2400, rm]  = gpib(address_2612b, address_2400)
    
    if test == 'iv':
        
        [readingsV_sipm, readingsI_sipm, 
         readingsR] = IVComplete(smu_2612b, smu_2400, config)
        
       
        smu_2612b.write('reset()')
            
        smu_2612b.write('smua.nvbuffer1.clear()')
        smu_2612b.write('smub.nvbuffer1.clear()') 
        smu_2400.write('*CLS')
            
        readingsV_sipm_neg, readingsV_sipm_pos, readingsI_sipm_neg, readingsI_sipm_pos, readingsR_neg, readingsR_pos = split(readingsV_sipm, readingsI_sipm, readingsR)
       
        number_neg = []
        number_pos = []
        
        for g in range(len(readingsR_neg)):
            number_neg.append(g)
            
        for g in range(len(readingsR_pos)):
            number_pos.append(g)
        
            
        if plotFlag == 1:
            graphR_neg = plot(number_neg, readingsR_neg, 'N', 'R', 1, log=False, errorbars_2400=True)
            graphR_pos = plot(number_pos, readingsR_pos, 'N', 'R', 2, log=False, errorbars_2400=True)
            graphIV_neg = plot(readingsV_sipm_neg, readingsI_sipm_neg, 'Vsipm', 'Isipm', 3, log=False, errorbars_2612=True)
            graphIV_pos = plot(readingsV_sipm_pos, readingsI_sipm_pos, 'Vsipm', 'Isipm', 4, log=False, errorbars_2612=True)
            
        else:
            graphR_neg = 'NULL'
            graphR_pos = 'NULL'
            graphIV_neg = 'NULL'
            graphIV_pos = 'NULL'
            
        if saveFlag == 1:
            group_path_pos = group_path + " (rq)"
            group_path_neg = group_path + " (vbr)"
            save_iv(readingsV_sipm_neg, readingsI_sipm_neg, readingsR_neg, graphIV_neg, 
                    graphR_neg, n, group_path_pos)
            
            save_iv(readingsV_sipm_pos, readingsI_sipm_pos, readingsR_pos, graphIV_pos, 
                    graphR_pos, n, group_path_neg)
         
        time.sleep(60)
        [readingsI_sipm, readingsR] = DarkCurrent(smu_2612b, smu_2400, config)
    
        smu_2612b.write('reset()')
            
        smu_2612b.write('smua.nvbuffer1.clear()')
        smu_2612b.write('smub.nvbuffer1.clear()') 
        smu_2400.write('*CLS')
        
        number = []
        for g in range(len(readingsR)):
            number.append(g)
        
        if plotFlag == 1:
            graphR = plot(number, readingsI_sipm, 'N', 'Isipm', 5, log=False, errorbars_2612=True)
        else:
            graphR = 'NULL'  
            
        if saveFlag == 1:
            group_path_dark = group_path + " (idark)"
            save_dark(readingsI_sipm, readingsR, graphR, n, group_path_dark)
    
        rm.close
        return 

    
    elif test == 'self_heating':
      
    
        [readingsV_sipm, readingsI_sipm, readingsV_led, 
         readingsI_led, readingsR] = SelfHeating(smu_2612b, smu_2400, config)
        
       
        smu_2612b.write('reset()')
            
        smu_2612b.write('smua.nvbuffer1.clear()')
        smu_2612b.write('smub.nvbuffer1.clear()') 
        smu_2400.write('*CLS')
            
        rm.close
        
        Number = []
        for i in range(0, len(readingsR)):
            Number.append(i)    
            
        
        if plotFlag == 1:
            graphR = plot(Number, readingsR, 'N', 'R', 1)
            graphIV = plot(readingsI_led, readingsI_sipm, 'Iled', 'Isipm', 2, log=True, errorbars_2612=True)
            
        else:
            graphR = 'NULL'
            graphIV = 'NULL'
            
        if saveFlag == 1:
            save(readingsV_sipm, readingsI_sipm, readingsV_led, readingsI_led, 
                 readingsR, graphIV, graphR, n, group_path)
    
        return 
    
    else:
        print(str(test) + " is not a valid mode")
        return
