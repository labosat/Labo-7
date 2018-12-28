from functions import cast, readBuffer, P, ThermostatInitial, Thermostat
import time

def IVComplete(smu_2612b, config):
    
    """
    
    
    
    ---------
    
    """
    
    [i_cc_sipm,
    v_cc_sipm,
    i_rang_sipm,
    v_rang_sipm,
    v_level_sipm,
    i_cc_led,
    v_cc_led,
    i_rang_led,
    v_rang_led,
    vStart,
    vEnd,
    return_sweep,
    N,
    points,
    delay,
    curves] = config
     
     
    i_led_level = 210*P('u')
    
    NPLC = round(points*200*P('u')*50, 2)
    
    smu_2612b.write('smua.reset()')
    smu_2612b.write('smub.reset()')
    
    smu_2612b.write('format.data = format.ASCII')
    
    # Buffer operations -------------------------------------------------------
    
    smu_2612b.write('smua.nvbuffer1.clear()')
    smu_2612b.write('smub.nvbuffer1.clear()')
    
    smu_2612b.write('smua.nvbuffer1.appendmode = 1')
    smu_2612b.write('smub.nvbuffer1.appendmode = 1')
    
    smu_2612b.write('smua.nvbuffer1.collectsourcevalues = 1')
    smu_2612b.write('smub.nvbuffer1.collectsourcevalues = 1')

    smu_2612b.write('smua.measure.count = 1')
    smu_2612b.write('smub.measure.count = 1')
    

    # -------------------------------------------------------------------------   
    # smua configuration (SiPM)
    
    smu_2612b.write('smua.source.func = smua.OUTPUT_DCVOLTS')
    smu_2612b.write('display.smua.measure.func = display.MEASURE_DCAMPS')
    
    if (i_rang_sipm == 'AUTO'):
        smu_2612b.write('smua.source.autorangei = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.source.rangei = ' + str(i_rang_sipm))
    
    if (v_rang_sipm == 'AUTO'):
        smu_2612b.write('smua.measure.autorangev = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.measure.rangev = ' + str(v_rang_sipm))

    #compliance values for I and V
    smu_2612b.write('smua.source.limiti = ' + str(i_cc_sipm))
    smu_2612b.write('smua.source.limitv = ' + str(v_cc_sipm))
	
    smu_2612b.write('smua.measure.nplc = ' + str(NPLC))
    
    smu_2612b.write('smua.measure.delay = ' + str(delay))
    
    # -------------------------------------------------------------------------   
    # smua configuration (SiPM)
    
    smu_2612b.write('smub.source.func = smub.OUTPUT_DCAMPS')
    smu_2612b.write('display.smub.measure.func = display.MEASURE_DCVOLTS')
    
    if (i_rang_led == 'AUTO'):
        smu_2612b.write('smub.source.autorangei = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangei = ' + str(i_rang_led))
    
    if (v_rang_led == 'AUTO'):
        smu_2612b.write('smub.measure.autorangev = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.measure.rangev = ' + str(v_rang_led))

    #compliance values for I and V
    smu_2612b.write('smub.source.limiti = ' + str(i_cc_led))
    smu_2612b.write('smub.source.limitv = ' + str(v_cc_led))
    
    smu_2612b.write('smub.source.leveli = ' + str(0))
        
        
    import numpy as np
    
    # allowed voltage values in sweep
    b = np.arange(0, N, 1)
    v_sipm_values1 = [vStart - (vStart)/N*i for i in b]
    v_sipm_values2 = [20 + (vEnd - 20)/N*i for i in b]
   
    v_sipm_values = np.concatenate((v_sipm_values1, v_sipm_values2))

    smu_2612b.write('smua.source.output = smua.OUTPUT_ON')
    
    print("Start of measurement")
    
    for i in range(0, curves):
    
        #startTime = time.time()
        for j in range(len(v_sipm_values)):
            
            smu_2612b.write('smua.source.levelv = ' + str(v_sipm_values[j]))
            smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
            
            if j != len(v_sipm_values) - 1:
                if (v_sipm_values[j + 1] - v_sipm_values[j]) > 10:
                        smu_2612b.write('smub.source.output = smub.OUTPUT_ON') 
                        smu_2612b.write('smub.source.leveli = ' + str(i_led_level)) 
                
    
    
        smu_2612b.write('waitcomplete()')
        smu_2612b.write('smub.source.leveli = ' + str(0)) 
        
        if return_sweep == 1:
            
            n = len(v_sipm_values)
            for j in range(len(v_sipm_values)):
                
                smu_2612b.write('smua.source.levelv = ' + str(v_sipm_values[n - j - 1]))
                smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
                
                if j != len(v_sipm_values) - 1:
                    if (v_sipm_values[j + 1] - v_sipm_values[j]) > 10:
                       smu_2612b.write('smub.source.leveli = ' + str(i_led_level)) 

    
            smu_2612b.write('waitcomplete()')
            smu_2612b.write('smub.source.leveli = ' + str(0)) 
            
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    
    print("End of measurement")
    
    readingsV_sipm = cast(readBuffer(smu_2612b, 'a')[1])
    readingsI_sipm = cast(readBuffer(smu_2612b, 'a')[0]) 

    return [readingsV_sipm, readingsI_sipm]
        

def DarkCurrent(smu_2612b, config):
    
        
    """
    
    
    
    ---------
    
    """
    
    [i_cc_sipm,
    v_cc_sipm,
    i_rang_sipm,
    v_rang_sipm,
    v_level_sipm,
    i_cc_led,
    v_cc_led,
    i_rang_led,
    v_rang_led,
    iStart,
    iEnd,
    return_sweep,
    N,
    points,
    delay,
    curves] = config
     
    NPLC = 25
    
    smu_2612b.write('smua.reset()')
    smu_2612b.write('smub.reset()')
    
    smu_2612b.write('format.data = format.ASCII')
    
    # Buffer operations -------------------------------------------------------
    
    smu_2612b.write('smua.nvbuffer1.clear()')
    smu_2612b.write('smub.nvbuffer1.clear()')
    
    smu_2612b.write('smua.nvbuffer1.appendmode = 1')
    smu_2612b.write('smub.nvbuffer1.appendmode = 1')
    
    smu_2612b.write('smua.nvbuffer1.collectsourcevalues = 1')
    smu_2612b.write('smub.nvbuffer1.collectsourcevalues = 1')

    smu_2612b.write('smua.measure.count = 1')
    smu_2612b.write('smub.measure.count = 1')
    

    # -------------------------------------------------------------------------   
    # smua configuration (SiPM)
    
    smu_2612b.write('smua.source.func = smua.OUTPUT_DCVOLTS')
    smu_2612b.write('display.smua.measure.func = display.MEASURE_DCAMPS')
    
    if (i_rang_sipm == 'AUTO'):
        smu_2612b.write('smua.source.autorangei = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.source.rangei = ' + str(i_rang_sipm))
    
    if (v_rang_sipm == 'AUTO'):
        smu_2612b.write('smua.measure.autorangev = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.measure.rangev = ' + str(v_rang_sipm))

    #compliance values for I and V
    smu_2612b.write('smua.source.limiti = ' + str(i_cc_sipm))
    smu_2612b.write('smua.source.limitv = ' + str(v_cc_sipm))
	
    smu_2612b.write('smua.measure.nplc = ' + str(NPLC))
    
    smu_2612b.write('smua.source.levelv = 30')
    
    smu_2612b.write('smua.measure.delay = ' + str(delay))
        
    # -------------------------------------------------------------------------
    
    smu_2612b.write('smua.source.output = smua.OUTPUT_ON') 

    
    print("Start of measurement")
    
    for j in range(10):
        smu_2612b.write('smua.measure.i(smua.nvbuffer1)')

    smu_2612b.write('waitcomplete()')
        
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    
    print("End of measurement")
    
    readingsI_sipm = cast(readBuffer(smu_2612b, 'a')[0]) 

    return readingsI_sipm

    
def LEDTest(smu_2612b, config):
        
    """
    
    
    
    ---------
    
    """
    
    [i_cc_sipm,
    v_cc_sipm,
    i_rang_sipm,
    v_rang_sipm,
    v_level_sipm,
    i_cc_led,
    v_cc_led,
    i_rang_led,
    v_rang_led,
    iStart,
    iEnd,
    return_sweep,
    N,
    points,
    delay,
    curves] = config
    
    NPLC = round(points*200*P('u')*50, 2)
    
    smu_2612b.write('smua.reset()')
    smu_2612b.write('smub.reset()')
    
    smu_2612b.write('format.data = format.ASCII')
    
    # Buffer operations -------------------------------------------------------
    
    smu_2612b.write('smua.nvbuffer1.clear()')
    smu_2612b.write('smub.nvbuffer1.clear()')
    
    smu_2612b.write('smua.nvbuffer1.appendmode = 1')
    smu_2612b.write('smub.nvbuffer1.appendmode = 1')
    
    smu_2612b.write('smua.nvbuffer1.collectsourcevalues = 1')
    smu_2612b.write('smub.nvbuffer1.collectsourcevalues = 1')

    smu_2612b.write('smua.measure.count = 1')
    smu_2612b.write('smub.measure.count = 1')
    

    # -------------------------------------------------------------------------   
    # smua configuration (SiPM)
    
    smu_2612b.write('smua.source.func = smua.OUTPUT_DCVOLTS')
    smu_2612b.write('display.smua.measure.func = display.MEASURE_DCAMPS')
    
    if (i_rang_sipm == 'AUTO'):
        smu_2612b.write('smua.source.autorangei = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.source.rangei = ' + str(i_rang_sipm))
    
    if (v_rang_sipm == 'AUTO'):
        smu_2612b.write('smua.measure.autorangev = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.measure.rangev = ' + str(v_rang_sipm))

    #compliance values for I and V
    smu_2612b.write('smua.source.limiti = ' + str(i_cc_sipm))
    smu_2612b.write('smua.source.limitv = ' + str(v_cc_sipm))
	
    smu_2612b.write('smua.measure.nplc = ' + str(NPLC))
    
    smu_2612b.write('smua.source.levelv = 30')
    
    # -------------------------------------------------------------------------   
    # smua configuration (SiPM)
    
    smu_2612b.write('smub.source.func = smub.OUTPUT_DCAMPS')
    smu_2612b.write('display.smub.measure.func = display.MEASURE_DCVOLTS')
    
    if (i_rang_led == 'AUTO'):
        smu_2612b.write('smub.source.autorangei = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangei = ' + str(i_rang_led))
    
    if (v_rang_led == 'AUTO'):
        smu_2612b.write('smub.measure.autorangev = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.measure.rangev = ' + str(v_rang_led))

    #compliance values for I and V
    smu_2612b.write('smub.source.limiti = ' + str(i_cc_led))
    smu_2612b.write('smub.source.limitv = ' + str(v_cc_led))
    
    smu_2612b.write('smub.measure.nplc = ' + str(NPLC))
    
    smu_2612b.write('smub.measure.delay = ' + str(delay))
        
        
    import numpy as np
    
    # allowed voltage values in sweep
    b = np.arange(0, N, 1)
    i_led_values1 = [iStart - (iStart)/N*i for i in b]
    i_led_values2 = [20 + (iEnd - 20)/N*i for i in b]
    
    #can code i_led_values with log scale
   
    i_led_values = np.concatenate((i_led_values1, i_led_values2))

    smu_2612b.write('smua.source.output = smua.OUTPUT_ON')
    
    print("Start of measurement")
    
    for i in range(0, curves):
    
        #startTime = time.time()
        for j in range(len(i_led_values)):
            
            smu_2612b.write('smub.source.leveli = ' + str(i_led_values[j]))
            smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
                    
        smu_2612b.write('waitcomplete()')
        smu_2612b.write('smub.source.leveli = ' + str(0)) 
        
        if return_sweep == 1:
            
            n = len(i_led_values)
            for j in range(len(i_led_values)):
                
                smu_2612b.write('smub.source.leveli = ' + str(i_led_values[n - j - 1]))
                smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
    
            smu_2612b.write('waitcomplete()')
            
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    
    print("End of measurement")
    
    readingsI_sipm = cast(readBuffer(smu_2612b, 'a')[0])
    readingsI_led = cast(readBuffer(smu_2612b, 'b')[1]) 
    readingsV_led = cast(readBuffer(smu_2612b, 'b')[0]) 

    return [readingsI_sipm, readingsI_led, readingsV_led]
