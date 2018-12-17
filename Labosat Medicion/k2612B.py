from functions import clear_all, gpib, plot, save, P
from setup import setup
from tests import SelfHeating, SelfHeatingThermostat

def run(n, group_path, plotFlag, saveFlag):

    # Loading setups configurations
    config = setup()
    
    #rm-list_resources() to find address for smu
    address_2612b = 26
    address_2400 = 24
    
    clear_all()
    
    #running tests (smua measures iv and smub measures r)
    
    [smu_2612b, smu_2400, rm]  = gpib(address_2612b, address_2400)
      
    
    [readingsV_sipm, readingsI_sipm, readingsV_led, readingsI_led, 
     readingsR] = SelfHeating(smu_2612b,
                                          smu_2400,
                                          config[0],
                                          config[1],
                                          config[2],
                                          config[3],
                                          config[4],
                                          config[5],
                                          config[6],
                                          config[7],
                                          config[8],
                                          config[9],
                                          config[10],
                                          config[11],
                                          config[12],
                                          config[13],
                                          config[14],
                                          config[15],
                                          config[16],
                                          config[17],
                                          config[18],
                                          config[19],
                                          config[20],
                                          config[21])
    
   
    smu_2612b.write('reset()')
        
    smu_2612b.write('smua.nvbuffer1.clear()')
    smu_2612b.write('smub.nvbuffer1.clear()') 
    smu_2400.write('*CLS')
        
    rm.close
    
    Number = []
    led_power = []
    for i in range(0, len(readingsR)):
        Number.append(i)
        led_power.append(readingsV_led[i]*readingsI_led[i])
        
        
    
    if plotFlag == 1:
        graphR = plot(Number, readingsR, 'N', 'R', 1)
        graphIV = plot(readingsI_led, readingsI_sipm, 'Iled', 'Isipm', 2, log=True, errorbars_2612=True)
        graphIVLed = plot(readingsV_led, readingsI_led, 'Vled', 'I', 3)
        
    else:
        graphR = 'NULL'
        graphIV = 'NULL'
        
    if saveFlag == 1:
        save(readingsV_sipm, readingsI_sipm, readingsV_led, readingsI_led, 
             readingsR, graphIV, graphR, n, group_path)

    return 
