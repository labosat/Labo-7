from functions import clear_all, gpib, plot, save_iv, save_dark, save_led, split
from setup import setup
from tests import IVComplete, DarkCurrent, LEDTest
import time

def run(n, test, group_path, plotFlag, saveFlag):

    clear_all()
    # Loading setups configurations
    config = setup()
    
    #rm-list_resources() to find address for smu
    address_2612b = 26
    
    #running tests (smua measures iv and smub measures r)
    
    [smu_2612b, rm]  = gpib(address_2612b)
    
    
    [readingsV_sipm, readingsI_sipm] = IVComplete(smu_2612b, config)
        
    readingsV_sipm_neg, readingsV_sipm_pos, readingsI_sipm_neg, readingsI_sipm_pos = split(readingsV_sipm, readingsI_sipm)
    
        
    if plotFlag == 1:
        graphIV_neg = plot(readingsV_sipm_neg, readingsI_sipm_neg, 'Vsipm', 'Isipm', 1, log=False, errorbars_2612=True)
        graphIV_pos = plot(readingsV_sipm_pos, readingsI_sipm_pos, 'Vsipm', 'Isipm', 2, log=False, errorbars_2612=True)
        
    else:
        graphIV_neg = 'NULL'
        graphIV_pos = 'NULL'
        
    if saveFlag == 1:
        group_path_pos = group_path + " (rq)"
        group_path_neg = group_path + " (vbr)"
        save_iv(readingsV_sipm_neg, readingsI_sipm_neg, graphIV_neg, n, group_path_pos)
        
        save_iv(readingsV_sipm_pos, readingsI_sipm_pos, graphIV_pos, n, group_path_neg)
     
    time.sleep(0)
    readingsI_sipm_dark = DarkCurrent(smu_2612b, config)
    
    number = []
    for g in range(len(readingsI_sipm_dark)):
        number.append(g)
    
    if plotFlag == 1:
        graphIV = plot(number, readingsI_sipm_dark, 'N', 'Isipm', 3, log=False, errorbars_2612=True)
    else:
        graphIV = 'NULL'  
        
    if saveFlag == 1:
        group_path_dark = group_path + " (idark)"
        save_dark(readingsI_sipm_dark, graphIV, n, group_path_dark)
        
    
    [readingsI_sipm_led, readingsI_led, readingsV_led] = LEDTest(smu_2612b, config)
    
    if plotFlag == 1:
        graphIV_led = plot(readingsI_led, readingsI_sipm_led, 'Iled', 'Isipm', 4, log=True, errorbars_2612=True, xflag='I')
    else:
        graphIV_led = 'NULL'  
        
    if saveFlag == 1:
        group_path_dark = group_path + " (LED)"
        save_led(readingsI_sipm_led, readingsI_led, readingsV_led, graphIV_led, n, group_path_dark)

    rm.close
    
    return 

    
