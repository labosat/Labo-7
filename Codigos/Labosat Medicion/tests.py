from functions import cast, readBuffer, P, ThermostatInitial, Thermostat
import time


def SelfHeating(smu_2612b, smu_2400, i_cc_sipm, v_cc_sipm, 
                i_rang_sipm, v_rang_sipm, v_level_sipm, i_cc_led, 
                v_cc_led, i_rang_led, v_rang_led, iStart, iEnd, 
                fourWire, i_cc_rtd, v_cc_rtd, i_rang_rtd, r_rang_rtd, 
                i_level_rtd, return_sweep, N, points, delay, curves):
    
    """
    
    
    
    ---------
    
    """
    
    NPLC = round(points*200*P('u')*50, 2)

    readingsR = []
    
    smu_2612b.write('smua.reset()')
    smu_2612b.write('smub.reset()')
    smu_2400.write("*RST")
    
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
    # smua configuration
    
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
	
    smu_2612b.write('smua.source.levelv = ' + str(v_level_sipm))
	
    smu_2612b.write('smua.measure.nplc = ' + str(NPLC))

    # -------------------------------------------------------------------------
    # smub configuration
    
    smu_2612b.write('smub.source.func = smub.OUTPUT_DCAMPS')
    
    if (i_rang_led == 'AUTO'):
        smu_2612b.write('smub.source.autorangei = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangei = ' + str(i_rang_led))
        
    if (v_rang_led == 'AUTO'):
        smu_2612b.write('smub.source.autorangev = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangev = ' + str(v_rang_led))

    #compliance values for I and V
    smu_2612b.write('smub.source.limiti = ' + str(i_cc_led))
    smu_2612b.write('smub.source.limitv = ' + str(v_cc_led))
	
#    smu_2612b.write('smub.measure.delay = ' + str(delay))
	

    #smu_2612b.write('smub.measure.nplc = ' + str(NPLC))
        
    # -------------------------------------------------------------------------
    # k2400 configuration (R measurement)

    smu_2400.write(':SENS:FUNC "RES"')
    smu_2400.write(':SOUR:FUNC CURR')
    smu_2400.write('SENS:RES:MODE MAN')
	
    if (i_rang_rtd == 'AUTO'):
        smu_2400.write(':SOUR:CURR:RANG:AUTO ON')
    else:
        smu_2400.write(':SOUR:CURR:RANG ' + str(i_rang_rtd))
		
    if (r_rang_rtd == 'AUTO'):
        smu_2400.write(':SENS:RES:RANG:AUTO ON')
    else:
        smu_2400.write(':SENS:RES:RANG ' + str(r_rang_rtd))
	   

    smu_2400.write(':SOUR:CURR:LEV ' + str(i_level_rtd))
    
    smu_2400.write('SENS:CURR:PROT ' + str(i_cc_rtd))
    smu_2400.write('SENS:VOLT:PROT ' + str(v_cc_rtd))
    
    #smu_2400.write('SENS:CURR:NPLC ' + str(1))
	
    if fourWire:
		smu_2400.write(':SYST:RSEN ON')
	   
    
    # -------------------------------------------------------------------------
    # Measurement -------------------------------------------------------------
	
    import numpy as np
    
    #calculates logarithmic current sweep
#    a = (1.0/(N - 1)) * np.log10(iEnd / iStart)
    b = np.arange(0, N, 1)
#    i_led_values = [iStart * 10**(i*a) for i in b]
    i_led_values = [iStart + (iEnd - iStart)/N*i for i in b]

    smu_2612b.write('smua.source.output = smua.OUTPUT_ON') 
    smu_2612b.write('smub.source.output = smub.OUTPUT_ON')
    
    smu_2400.write('OUTP ON')
    
    print("Start of measurement")
    
    for i in range(0, curves):
    
        #startTime = time.time()
        for j in range(len(i_led_values)):
            
            smu_2612b.write('smub.source.leveli = ' + str(i_led_values[j]))
            smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
            smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
            
            auxRead = smu_2400.query(':READ?')
            rtd_r = float(cast(auxRead)[2])
            readingsR.append(rtd_r)
            time.sleep(delay + NPLC/50.)
    
    
        smu_2612b.write('waitcomplete()')
    
        
        if return_sweep == 1:
            
            n = len(i_led_values)
            for j in range(len(i_led_values)):
                
                smu_2612b.write('smub.source.leveli = ' + str(i_led_values[n - j - 1]))
                smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
                smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
                            
                auxRead = smu_2400.query(':READ?')
                rtd_r = float(cast(auxRead)[2])
                readingsR.append(rtd_r)
                time.sleep(delay + NPLC/50.)

    
        smu_2612b.write('waitcomplete()')
        
#        #startTime = time.time()
#        for j in range(len(i_led_values)):
#            
#            smu_2612b.write('smub.source.leveli = ' + str(i_led_values[j]))
#            smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
#            smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
#            
#            auxRead = smu_2400.query(':READ?')
#            rtd_r = float(cast(auxRead)[2])
#            readingsR.append(rtd_r)
#            time.sleep(delay + NPLC/50.)
#    
#    
#        smu_2612b.write('waitcomplete()')
#    
#        
#        if return_sweep == 1:
#            
#            n = len(i_led_values)
#            for j in range(len(i_led_values)):
#                
#                smu_2612b.write('smub.source.leveli = ' + str(i_led_values[n - j - 1]))
#                smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
#                smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
#                            
#                auxRead = smu_2400.query(':READ?')
#                rtd_r = float(cast(auxRead)[2])
#                readingsR.append(rtd_r)
#                time.sleep(delay + NPLC/50.)
#
#    
#        smu_2612b.write('waitcomplete()')
            
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('OUTP OFF')
    
    print("End of measurement")
    
    readingsV_sipm = cast(readBuffer(smu_2612b, 'a')[1])
    readingsI_sipm = cast(readBuffer(smu_2612b, 'a')[0])
    
    readingsV_led = cast(readBuffer(smu_2612b, 'b')[0])
    readingsI_led = cast(readBuffer(smu_2612b, 'b')[1])
    

    return [readingsV_sipm, readingsI_sipm, readingsV_led, readingsI_led, 
            readingsR]




def SelfHeatingThermostat(smu_2612b, smu_2400, i_cc_sipm, v_cc_sipm, 
                i_rang_sipm, v_rang_sipm, v_level_sipm, i_cc_led, 
                v_cc_led, i_rang_led, v_rang_led, iStart, iEnd, 
                fourWire, i_cc_rtd, v_cc_rtd, i_rang_rtd, r_rang_rtd, 
                i_level_rtd, return_sweep, N, points, delay, curves):
    
    """
    
    
    
    ---------
    
    """
    
    NPLC = round(points*200*P('u')*50, 2)
    tolerance = 0.03

    readingsR = []
    
    smu_2612b.write('smua.reset()')
    smu_2612b.write('smub.reset()')
    smu_2400.write("*RST")
    
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
    # smua configuration
    
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
	
    smu_2612b.write('smua.source.levelv = ' + str(v_level_sipm))
	
    smu_2612b.write('smua.measure.nplc = ' + str(NPLC))

    # -------------------------------------------------------------------------
    # smub configuration
    
    smu_2612b.write('smub.source.func = smub.OUTPUT_DCAMPS')
    
    if (i_rang_led == 'AUTO'):
        smu_2612b.write('smub.source.autorangei = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangei = ' + str(i_rang_led))
        
    if (v_rang_led == 'AUTO'):
        smu_2612b.write('smub.source.autorangev = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangev = ' + str(v_rang_led))

    #compliance values for I and V
    smu_2612b.write('smub.source.limiti = ' + str(i_cc_led))
    smu_2612b.write('smub.source.limitv = ' + str(v_cc_led))
	
    smu_2612b.write('smub.measure.delay = ' + str(delay))
	

    #smu_2612b.write('smub.measure.nplc = ' + str(NPLC))
        
    # -------------------------------------------------------------------------
    # k2400 configuration (R measurement)

    smu_2400.write(':SENS:FUNC "RES"')
    smu_2400.write(':SOUR:FUNC CURR')
    smu_2400.write('SENS:RES:MODE MAN')
	
    if (i_rang_rtd == 'AUTO'):
        smu_2400.write(':SOUR:CURR:RANG:AUTO ON')
    else:
        smu_2400.write(':SOUR:CURR:RANG ' + str(i_rang_rtd))
		
    if (r_rang_rtd == 'AUTO'):
        smu_2400.write(':SENS:RES:RANG:AUTO ON')
    else:
        smu_2400.write(':SENS:RES:RANG ' + str(r_rang_rtd))
	   

    smu_2400.write(':SOUR:CURR:LEV ' + str(i_level_rtd))
    
    smu_2400.write('SENS:CURR:PROT ' + str(i_cc_rtd))
    smu_2400.write('SENS:VOLT:PROT ' + str(v_cc_rtd))
    
    #smu_2400.write('SENS:CURR:NPLC ' + str(1))
	
    if fourWire:
		smu_2400.write(':SYST:RSEN ON')
	   
    
    # -------------------------------------------------------------------------
    # Measurement -------------------------------------------------------------
	
    import numpy as np
    
    #calculates logarithmic current sweep
    a = (1.0/(N - 1)) * np.log10(iEnd / iStart)
    b = np.arange(0, N, 1)
    i_led_values = [iStart * 10**(i*a) for i in b]
    
    i_led_values = np.arange(iStart, iEnd, (iEnd - iStart)/N)
    

    smu_2612b.write('smua.source.output = smua.OUTPUT_ON') 
    smu_2612b.write('smub.source.output = smub.OUTPUT_ON')
    
    smu_2400.write('OUTP ON')
    
    print("Start of measurement")
    
    print("Measuring temperature")        
        
    condition = ThermostatInitial(smu_2400, tolerance)

    print("Temperature: " + str(condition - tolerance) + " \pm " + str(tolerance))
    
    #startTime = time.time()
    for j in range(len(i_led_values)):
        flag = True
        
        while flag:
            smu.write('OUTP ON')
            R_condition = cast(smu_2400.query(':READ?'))[2]
            if R_condition < (condition + tolerance) and R_condition > (condition - tolerance):
                smu_2612b.write('smub.source.leveli = ' + str(i_led_values[j]))
                smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
                smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
                
                auxRead = smu_2400.query(':READ?')
                rtd_r = float(cast(auxRead)[2])
                readingsR.append(rtd_r)
                time.sleep(delay)
                
                flag = False
            
            else:
                Thermostat(smu_2612b, R_condition, condition, tolerance, i_led_values[j])
        


    smu_2612b.write('waitcomplete()')

    
    if return_sweep == 1:
        
        n = len(i_led_values)
        for j in range(len(i_led_values)):
            flag = True
        
            while flag:
                R_condition = cast(smu_2400.query(':READ?'))[2]
                if R_condition < (condition + tolerance) and R_condition > (condition - tolerance):
                    smu_2612b.write('smub.source.leveli = ' + str(i_led_values[len(i_led_values) - 1 - j]))
                    smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
                    smu_2612b.write('smua.measure.i(smua.nvbuffer1)')
                    
                    auxRead = smu_2400.query(':READ?')
                    rtd_r = float(cast(auxRead)[2])
                    readingsR.append(rtd_r)
                    time.sleep(delay)
                    
                    flag = False
                
                else:
                    Thermostat(smu_2612b, R_condition, condition, tolerance, i_led_values[len(i_led_values) - 1 - j])


    smu_2612b.write('waitcomplete()')
            
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('OUTP OFF')
    
    print("End of measurement")
    
    readingsV_sipm = cast(readBuffer(smu_2612b, 'a')[1])
    readingsI_sipm = cast(readBuffer(smu_2612b, 'a')[0])
    
    readingsV_led = cast(readBuffer(smu_2612b, 'b')[0])
    readingsI_led = cast(readBuffer(smu_2612b, 'b')[1])
    

    return [readingsV_sipm, readingsI_sipm, readingsV_led, readingsI_led, 
            readingsR]



