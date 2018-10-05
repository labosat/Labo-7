import time
from functions import cast, readBuffer


def ivr(smu, fourWire, i_cca, v_cca, iRanga, vRanga, iLevela, i_ccb, v_ccb,
        iRangb, vRangb, vStart, vEnd, vStep, iStart, iEnd, iStep, source, NPLC, wait_time):
    
    """
    
    Function to control Keithley 2612B (IV and R measurement)
    
    ---------
    
    """
    
    readingsV = []
    readingsI = []
    readingsR = []
    
    smu.write('smua.reset()')
    smu.write('smub.reset()')
    
    smu.write('format.data = format.ASCII')
    
    # Buffer operations -------------------------------------------------------
    
    smu.write('smua.nvbuffer1.clear()')
    smu.write('smub.nvbuffer1.clear()')
    
    smu.write('smua.nvbuffer1.appendmode = 1')
    smu.write('smub.nvbuffer1.appendmode = 1')
    
    smu.write('smua.nvbuffer1.collectsourcevalues = 1')
    smu.write('smub.nvbuffer1.collectsourcevalues = 1')

    smu.write('smua.measure.count = 1')
    smu.write('smub.measure.count = 1')

    # -------------------------------------------------------------------------   
    # Smub (iv) configuration
    
    if (source == 'V'):
        smu.write('smub.source.func = smub.OUTPUT_DCVOLTS')
        smu.write('display.smub.measure.func = display.MEASURE_DCAMPS')
        
        if (iRangb == 'AUTO'):
            smu.write('smub.measure.autorangei = smub.AUTORANGE_ON')
        else:
            smu.write('smub.measure.rangei = ' + str(iRangb))
        
        if (vRangb == 'AUTO'):
            smu.write('smub.source.autorangev = smub.AUTORANGE_ON')
        else:
            smu.write('smub.source.rangev = ' + str(vRangb))
    
        smu.write('smub.source.levelv = ' + str(vStart))
    
        #compliance values for I and V
        smu.write('smub.source.limiti = ' + str(i_ccb))
        smu.write('smub.source.limitv = ' + str(v_ccb))
        
    elif (source == 'I'):
        smu.write('smub.source.func = smub.OUTPUT_DCAMPS')
        #smu.write('display.smua.measure.func = display.MEASURE_DCVOLTS')
        
        if (iRangb == 'AUTO'):
            smu.write('smub.source.autorangei = smub.AUTORANGE_ON')
        else:
            smu.write('smub.source.rangei = ' + str(iRangb))
        
        if (vRangb == 'AUTO'):
            smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
        else:
            smu.write('smub.measure.rangev = ' + str(vRangb))
    
        smu.write('smub.source.leveli = ' + str(iStart))
    
        #compliance values for I and V
        smu.write('smub.source.limiti = ' + str(i_ccb))
        smu.write('smub.source.limitv = ' + str(v_ccb))        
    
    else:
        print(str(source) + " is not a valid source")
        return
    
   
    #sets the ADC speed to NPLC
    smu.write('smub.measure.nplc = ' + str(NPLC))
    
    # -------------------------------------------------------------------------
    # smua (r) configuration
    
    smu.write('smua.source.func = smua.OUTPUT_DCAMPS')
    
    if (iRanga == 'AUTO'):
        smu.write('smua.source.autorangei = smua.AUTORANGE_ON')
    else:
        smu.write('smua.source.rangei = ' + str(iRanga))
        
    if (vRanga == 'AUTO'):
        smu.write('smua.source.autorangev = smua.AUTORANGE_ON')
    else:
        smu.write('smua.source.rangev = ' + str(vRanga))
    
    smu.write('smua.source.leveli = ' + str(iLevela))

    #compliance values for I and V
    smu.write('smua.source.limiti = ' + str(i_cca))
    smu.write('smua.source.limitv = ' + str(v_cca))

    if (fourWire == 1):
        smu.write('smua.sense = smua.SENSE_REMOTE')
       
    
    # -------------------------------------------------------------------------
    # Measurement -------------------------------------------------------------

    
    smu.write('smua.source.output = smua.OUTPUT_ON') 
    smu.write('smub.source.output = smub.OUTPUT_ON')
    
    print("Start of measurement")
    
    if (source == 'V'):
        v = vStart
        #startTime = time.time()
        while (v <= vEnd):
            smu.write('smub.source.levelv = ' + str(v))
            time.sleep(wait_time)
            smu.write('smub.measure.i(smub.nvbuffer1)')
            smu.write('smua.measure.r(smua.nvbuffer1)')
            v += vStep
    
    elif (source == 'I'):    
        i = iStart
        #startTime = time.time()
        while (i <= iEnd):
            smu.write('smub.source.leveli = ' + str(i))
            time.sleep(wait_time)
            smu.write('smub.measure.v(smub.nvbuffer1)')
            smu.write('smua.measure.r(smua.nvbuffer1)')
            i += iStep
    
    #80 is the number of measurements for vbr
    time.sleep(4 + wait_time*100)
    smu.write('smua.source.output = smua.OUTPUT_OFF')
    smu.write('smub.source.output = smub.OUTPUT_OFF')
    #endTime = time.time() - startTime
    
    print("End of measurement")
    #print("Elapsed time: " + str(endTime))
    #print("Press Enter to continue...")
    #enter = raw_input()
    
    if (source == 'V'):
        readingsV_temp = readBuffer(smu, 'b')[1]
        readingsI_temp = readBuffer(smu, 'b')[0]
    elif (source == 'I'):
        readingsV_temp = readBuffer(smu, 'b')[0]
        readingsI_temp = readBuffer(smu, 'b')[1]
    
    
    readingsR_temp = readBuffer(smu, 'a')[0]
    readingsIR_temp = readBuffer(smu, 'a')[1]
    
    readingsV = cast(readingsV_temp)
    readingsI = cast(readingsI_temp)
    readingsR = cast(readingsR_temp)
    readingsIR = cast(readingsIR_temp)

    return [readingsV, readingsI, readingsR, readingsIR]



def led1(smu_2612b, smu_2400, fourWire, i_cca, v_cca, iRanga, vRanga, iLevela, 
        i_ccb, v_ccb, iRangb, vRangb, iStart, iEnd, iStep, return_sweep,
        vPolarization_sipm, wait_time):
    
    """
    
    Function to control Keithley 2612B (I_led and R measurement) and Keithley 2400 
    (I_Sipm measurement). This function performs a current sweep on the led while
    measuring I on Sipm polarized with a fixed voltage. Format of (iv) data is
    I_sipm, V_led, I_led
    
    ---------
    
    """
    
    readingsI_sipm = []
    readingsV_led = []
    readingsI_led = []
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
    # Smub (iv) configuration
    
    smu_2612b.write('smub.source.func = smub.OUTPUT_DCAMPS')
    #smu_2612b.write('display.smub.measure.func = display.MEASURE_DCVOLTS')
    
    if (iRangb == 'AUTO'):
        smu_2612b.write('smub.source.autorangei = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangei = ' + str(iRangb))
    
    if (vRangb == 'AUTO'):
        smu_2612b.write('smub.measure.autorangev = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.measure.rangev = ' + str(vRangb))

    #compliance values for I and V
    smu_2612b.write('smub.source.limiti = ' + str(i_ccb))
    smu_2612b.write('smub.source.limitv = ' + str(v_ccb))

    # -------------------------------------------------------------------------
    # smua (r) configuration
    
    smu_2612b.write('smua.source.func = smua.OUTPUT_DCAMPS')
    
    if (iRanga == 'AUTO'):
        smu_2612b.write('smua.source.autorangei = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.source.rangei = ' + str(iRanga))
        
    if (vRanga == 'AUTO'):
        smu_2612b.write('smua.source.autorangev = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.source.rangev = ' + str(vRanga))
    
    smu_2612b.write('smua.source.leveli = ' + str(iLevela))

    #compliance values for I and V
    smu_2612b.write('smua.source.limiti = ' + str(i_cca))
    smu_2612b.write('smua.source.limitv = ' + str(v_cca))

    if (fourWire == 1):
        smu_2612b.write('smua.sense = smua.SENSE_REMOTE')
        
    # -------------------------------------------------------------------------
    # k2400 configuration (Sipm measurement)

    
    smu_2400.write(':SENS:FUNC "CURR"')
    smu_2400.write(':SOUR:FUNC VOLT')
    smu_2400.write(':SENS:CURR:RANG:AUTO ON')
    smu_2400.write(':SENS:VOLT:RANG:AUTO ON')
    
    #compliance current
    smu_2400.write(':SOUR:VOLT:LEV ' + str(vPolarization_sipm))
    #protection for sipm is 18mA
    smu_2400.write('SENS:CURR:PROT ' + str(0.018))
       
    
    # -------------------------------------------------------------------------
    # Measurement -------------------------------------------------------------

    
    smu_2612b.write('smua.source.output = smua.OUTPUT_ON') 
    smu_2612b.write('smub.source.output = smub.OUTPUT_ON')
    
    smu_2400.write('OUTP ON')
    
    print("Start of measurement")
    
    i = iStart
    #startTime = time.time()
    while (i <= iEnd):
        smu_2612b.write('smub.source.leveli = ' + str(i))
        time.sleep(wait_time)
        smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
        smu_2612b.write('smua.measure.r(smua.nvbuffer1)')

        auxRead = smu_2400.query(':READ?')
        sipm_current = float(cast(auxRead)[1])
        
        readingsI_sipm.append(sipm_current)
        
        if i != iEnd:
            i += iStep
        

    #see about this waiting time...
    #time.sleep(4.5)
    
    i -= iStep
    
    if return_sweep == 1:
        while (i >= iStart):
            smu_2612b.write('smub.source.leveli = ' + str(i))
            time.sleep(wait_time)
            smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
            smu_2612b.write('smua.measure.r(smua.nvbuffer1)')

            auxRead = smu_2400.query(':READ?')
            sipm_current = float(cast(auxRead)[1])
        
            readingsI_sipm.append(sipm_current)
        
            i -= iStep
            
        #time.sleep(4.5)
    
    
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('OUTP OFF')
    #endTime = time.time() - startTime
    
    print("End of measurement")
    #print("Elapsed time: " + str(endTime))
    #print("Press Enter to continue...")
    #enter = raw_input()
    
    readingsI_led_temp = readBuffer(smu_2612b, 'b')[1]
    readingsV_led_temp = readBuffer(smu_2612b, 'b')[0]
    
    readingsR_temp = readBuffer(smu_2612b, 'a')[0]
    readingsIR_temp = readBuffer(smu_2612b, 'a')[1]
    
    readingsI_led = cast(readingsI_led_temp)
    readingsV_led = cast(readingsV_led_temp)
    
    readingsR = cast(readingsR_temp)
    readingsIR = cast(readingsIR_temp)

    return [readingsI_sipm, readingsV_led, readingsI_led, readingsR, readingsIR]


def led2(smu_2612b, smu_2400, fourWire, i_cca, v_cca, iRanga, vRanga, iLevela, 
        i_ccb, v_ccb, iRangb, vRangb, vStart, vEnd, vStep, v_cc_led, iPolarization_led, 
        wait_time):
    
    """
    
    Function to control Keithley 2612B (I_sipm and R measurement) and Keithley 2400 
    (I_led and V_led measurement). This function performs a voltage sweep on the sipm while
    measuring I_sipm with a fixed current on the led. Data format in output is
    V_led, V_sipm, I_sipm
    
    ---------
    
    """
    
    readingsV_led = []
    readingsV_sipm = []
    readingsI_sipm = []
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
    # Smub (iv) configuration
    
    smu_2612b.write('smub.source.func = smub.OUTPUT_DCVOLTS')
    smu_2612b.write('display.smub.measure.func = display.MEASURE_DCAMPS')
    
    if (iRangb == 'AUTO'):
        smu_2612b.write('smub.measure.autorangei = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.measure.rangei = ' + str(iRangb))
    
    if (vRangb == 'AUTO'):
        smu_2612b.write('smub.source.autorangev = smub.AUTORANGE_ON')
    else:
        smu_2612b.write('smub.source.rangev = ' + str(vRangb))

    #compliance values for I and V
    smu_2612b.write('smub.source.limiti = ' + str(i_ccb))
    smu_2612b.write('smub.source.limitv = ' + str(v_ccb))

    # -------------------------------------------------------------------------
    # smua (r) configuration
    
    smu_2612b.write('smua.source.func = smua.OUTPUT_DCAMPS')
    
    if (iRanga == 'AUTO'):
        smu_2612b.write('smua.source.autorangei = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.source.rangei = ' + str(iRanga))
        
    if (vRanga == 'AUTO'):
        smu_2612b.write('smua.source.autorangev = smua.AUTORANGE_ON')
    else:
        smu_2612b.write('smua.source.rangev = ' + str(vRanga))
    
    smu_2612b.write('smua.source.leveli = ' + str(iLevela))

    #compliance values for I and V
    smu_2612b.write('smua.source.limiti = ' + str(i_cca))
    smu_2612b.write('smua.source.limitv = ' + str(v_cca))

    if (fourWire == 1):
        smu_2612b.write('smua.sense = smua.SENSE_REMOTE')
        
    # -------------------------------------------------------------------------
    # k2400 configuration (Sipm measurement)

    
    smu_2400.write(':SENS:FUNC "VOLT"')
    smu_2400.write(':SOUR:FUNC CURR')
    smu_2400.write(':SENS:CURR:RANG:AUTO ON')
    smu_2400.write(':SENS:VOLT:RANG:AUTO ON')
    
    #compliance current
    smu_2400.write(':SOUR:CURR:LEV ' + str(iPolarization_led))
    smu_2400.write(':SENS:VOLT:PROT ' + str(v_cc_led))
       
    
    # -------------------------------------------------------------------------
    # Measurement -------------------------------------------------------------

    
    smu_2612b.write('smua.source.output = smua.OUTPUT_ON') 
    smu_2612b.write('smub.source.output = smub.OUTPUT_ON')
    
    smu_2400.write('CHANNEL:OUTP ON')
    
    print("Start of measurement")
    
    v = vStart
    #startTime = time.time()
    while (v <= vEnd):
        smu_2612b.write('smub.source.levelv = ' + str(v))
        time.sleep(wait_time)
        smu_2612b.write('smub.measure.i(smub.nvbuffer1)')
        smu_2612b.write('smua.measure.r(smua.nvbuffer1)')

        auxRead = smu_2400.query(':READ?')
        led_voltage = float(auxRead)
        
        readingsV_led.append(led_voltage)
        
        v += vStep
        

    #see about this waiting time...
    time.sleep(4.5)
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('CHANNEL:OUTP OFF')
    #endTime = time.time() - startTime
    
    print("End of measurement")
    #print("Elapsed time: " + str(endTime))
    #print("Press Enter to continue...")
    #enter = raw_input()
    
    readingsI_sipm_temp = readBuffer(smu_2612b, 'b')[1]
    readingsV_sipm_temp = readBuffer(smu_2612b, 'b')[0]
    
    readingsR_temp = readBuffer(smu_2612b, 'a')[0]
    readingsIR_temp = readBuffer(smu_2612b, 'a')[1]
    
    readingsI_sipm = cast(readingsI_sipm_temp)
    readingsV_sipm = cast(readingsV_sipm_temp)
    
    readingsR = cast(readingsR_temp)
    readingsIR = cast(readingsIR_temp)

    return [readingsV_led, readingsV_sipm, readingsI_sipm, readingsR, readingsIR]
