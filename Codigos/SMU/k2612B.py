from functions import clear_all, gpib, gpib2, usb, plot, save, save_led, P
from setup import setup
from tests import ivr, led1, led2

def run(n, mode, group_path, plotFlag, saveFlag, wait_time):

    # Loading setups configurations
    config    = setup()
    
    #rm-list_resources() to find address for smu
    address_2612b = 26
    address_2400 = 24
    
    clear_all()
    
    #running tests (smua measures iv and smub measures r)
    
    if mode == 'iv':
        [smu, rm]  = gpib(address_2612b)
        
        [readingsV, readingsI, readingsR, readingsIR] = ivr(smu,
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
                                                            config[18],
                                                            wait_time)
    
    
        smu.write('reset()')
            
        smu.write('smua.nvbuffer1.clear()')
        smu.write('smub.nvbuffer1.clear()')   
            
        rm.close
        
        Number = []
        for i in range(0, len(readingsR)):
            Number.append(i)
        
        if plotFlag == 1:
            graphR = plot(Number, readingsR, 'N', 'R', 1)
            graphIV = plot(readingsV, readingsI, 'V', 'I', 2)
        else:
            graphR = 'NULL'
            graphIV = 'NULL'
            
        if saveFlag == 1:
            save(readingsV, readingsI, readingsR, readingsIR, 
                 graphIV, graphR, n, group_path)
            
        return
    
    elif mode == 'led1':
        
        [smu_2612b, smu_2400, rm]  = gpib2(address_2612b, address_2400)
        
        #polarization voltage for sipm on led1 test
        vPolarization_sipm = 30
        
        [readingsI_sipm, readingsV_led, readingsI_led, 
         readingsR, readingsIR] = led1(smu_2612b,
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
                                      config[13],
                                      config[14],
                                      config[15],
                                      vPolarization_sipm,
                                      wait_time)
        
       
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
            graphIV = plot(readingsI_led, readingsI_sipm, 'Iled', 'Isipm', 2)
        else:
            graphR = 'NULL'
            graphIV = 'NULL'
            
        if saveFlag == 1:
            save_led(readingsI_sipm, readingsV_led, readingsI_led, readingsR, 
                     readingsIR, graphIV, graphR, n, group_path)

        return
    
     
    elif mode == 'led2':
        
        [smu_2612b, smu_2400, rm]  = gpib2(address_2612b, address_2400)
        
        #polarization current for led on led2 test
        iPolarization_led = 100*P('m')
        
        [readingsV_led, readingsV_sipm, readingsI_sipm, 
         readingsR, readingsIR] = led1(smu_2612b,
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
                                      config[17],
                                      iPolarization_led,
                                      wait_time)
        
       
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
            graphIV = plot(readingsV_led, readingsI_sipm, 'Iled', 'Isipm', 2)
        else:
            graphR = 'NULL'
            graphIV = 'NULL'
            
        if saveFlag == 1:
            save_led(readingsV_led, readingsV_sipm, readingsI_sipm, readingsR, 
                     readingsIR, graphIV, graphR, n, group_path)

        return