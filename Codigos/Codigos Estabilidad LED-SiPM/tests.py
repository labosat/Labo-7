import time
from functions import cast, readBuffer, P, thermostatInitial, thermostat


def ivr(smu, fourWire, i_cca, v_cca, iRanga, vRanga, iLevela, i_ccb, v_ccb,
        iRangb, vRangb, vStart, vEnd, vStep, iStart, iEnd, iStep, source, 
        NPLC, wait_time):
    
    """
    
    Function to control Keithley 2612B for IV measurement on sipm and R measurement
    on rtd resistance. 
    
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
    
    Function to control Keithley 2612B (V_led and R measurement) and Keithley 2400 
    (I_Sipm measurement). This function performs a current sweep on the led while
    measuring I on Sipm polarized with a fixed voltage. Voltage can be set
    on k2612B.py under 'led1' section. Format of iv data is I_sipm, V_led, I_led.
    Data format of r data is R_rtd, I_rtd.
    
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
            
        #time.sleep(3)

    #--------------------------------------------------------------------------
        
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
            
            #time.sleep(3)
    
    
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('OUTP OFF')
    
    print("End of measurement")
    
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
        i_ccb, v_ccb, iRangb, vRangb, v_cc_led, measurements, vPolarization_sipm,
        iPolarization_led, wait_time, NPLC):
    
    """
    
    Function to control Keithley 2612B (I_sipm and R measurement) and Keithley 2400 
    (V_led measurement) for fixed current on led and fixed voltage on sipm. 
    This function measures I_sipm as a function of time to check sipm stability. 
    wait_time in this function serves the purpose of "time counter", not to wait 
    between measurements, so total time = measurements*wait_time.led current and
    sipm voltage can be set on k2612B.py under 'led2' section.
    Data format of iv data in output is time, I_sipm, V_led.
    Data format of r data is R_rtd, I_rtd.
    
    ---------
    
    """
    
    readingsV_led = []
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
    
    smu_2612b.write('smub.source.levelv = ' + str(vPolarization_sipm))

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
        
        
    #sets the ADC speed to NPLC
    smu_2612b.write('smub.measure.nplc = ' + str(NPLC))
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
    
    smu_2400.write('OUTP ON')
    
    print("Start of measurement")
    
    count = 0
    #startTime = time.time()
    while (count < measurements):
        smu_2612b.write('smub.measure.i(smub.nvbuffer1)')
        smu_2612b.write('smua.measure.r(smua.nvbuffer1)')

        auxRead = smu_2400.query(':READ?')
        led_voltage = float(cast(auxRead)[1])
        readingsV_led.append(led_voltage)
        
        count += 1
                
        #in this function, wait_time serves to measure time (not to wait 
        #between measurements)
        time.sleep(wait_time)
        
    time.sleep(4)
        
    #time.sleep(4.5)
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('OUTP OFF')
    #endTime = time.time() - startTime
    
    print("End of measurement")
    #print("Elapsed time: " + str(endTime))
    #print("Press Enter to continue...")
    #enter = raw_input()
    
    readingsI_sipm_temp = readBuffer(smu_2612b, 'b')[0]
    
    readingsR_temp = readBuffer(smu_2612b, 'a')[0]
    readingsIR_temp = readBuffer(smu_2612b, 'a')[1]
    
    readingsI_sipm = cast(readingsI_sipm_temp)
    
    readingsR = cast(readingsR_temp)
    readingsIR = cast(readingsIR_temp)

    return [readingsI_sipm, readingsV_led, readingsR, readingsIR]


def led3(smu_2612b, smu_2400, fourWire, i_cca, v_cca, iRanga, vRanga, iLevela, 
        i_ccb, v_ccb, iRangb, vRangb, vStart, vEnd, vStep, v_cc_led, return_sweep,
        iPolarization_led, wait_time):
    
    """
    
    Function to control Keithley 2612B (I_sipm and R measurement) and Keithley 2400 
    (I_led measurement). This function performs a voltage sweep on the sipm while
    measuring I, with led polarized with a fixed current. Format of iv data is 
    I_led, V_sipm, I_sipm. Data format of r data is R_rtd, I_rtd.
    
    ---------
    
    """
    
    readingsI_sipm = []
    readingsV_sipm = []
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
    
    smu_2612b.write('smub.source.func = smub.OUTPUT_DCVOLTS')
    smu_2612b.write('display.smub.measure.func = display.MEASURE_DCAMPS')
    
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

    
    smu_2400.write(':SENS:FUNC "VOLT"')
    smu_2400.write(':SOUR:FUNC CURR')
    smu_2400.write(':SENS:CURR:RANG:AUTO ON')
    smu_2400.write(':SENS:VOLT:RANG:AUTO ON')
    
    #compliance current
    smu_2400.write(':SOUR:CURR:LEV ' + str(iPolarization_led))
    #protection for sipm is 18mA
    smu_2400.write('SENS:VOLT:PROT ' + str(v_cc_led))
       
    
    smu_2612b.write('smua.source.output = smua.OUTPUT_ON') 
    smu_2612b.write('smub.source.output = smub.OUTPUT_ON')
    
    smu_2400.write('OUTP ON')
    
    print("Start of measurement")
    
    v = vStart
    #startTime = time.time()
    while (v <= vEnd):
        smu_2612b.write('smub.source.levelv = ' + str(v))
        time.sleep(wait_time)
        smu_2612b.write('smub.measure.i(smub.nvbuffer1)')
        smu_2612b.write('smua.measure.r(smua.nvbuffer1)')

        auxRead = smu_2400.query(':READ?')
        led_current = float(cast(auxRead)[1])
        
        readingsI_led.append(led_current)
        
        if v != vEnd:
            v += vStep
        
    
    v -= vStep
    
    if return_sweep == 1:
        while (v >= vStart):
            smu_2612b.write('smub.source.levelv = ' + str(v))
            time.sleep(wait_time)
            smu_2612b.write('smub.measure.i(smub.nvbuffer1)')
            smu_2612b.write('smua.measure.r(smua.nvbuffer1)')

            auxRead = smu_2400.query(':READ?')
            led_current = float(cast(auxRead)[1])
        
            readingsI_led.append(led_current)
        
            v -= vStep
    
    
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('OUTP OFF')
    
    print("End of measurement")
    
    readingsI_sipm_temp = readBuffer(smu_2612b, 'b')[0]
    readingsV_sipm_temp = readBuffer(smu_2612b, 'b')[1]
    
    readingsR_temp = readBuffer(smu_2612b, 'a')[0]
    readingsIR_temp = readBuffer(smu_2612b, 'a')[1]
    
    readingsI_sipm = cast(readingsI_sipm_temp)
    readingsV_sipm = cast(readingsV_sipm_temp)
    
    readingsR = cast(readingsR_temp)
    readingsIR = cast(readingsIR_temp)

    return [readingsI_led, readingsV_sipm, readingsI_sipm,
            readingsR, readingsIR]

def led4(smu_2612b, smu_2400, fourWire, i_cca, v_cca, iRanga, vRanga, iLevela, 
        i_ccb, v_ccb, iRangb, vRangb, iStart, iEnd, iStep, return_sweep,
        vPolarization_sipm, wait_time, tolerance):
    
    """
    
    Function to control Keithley 2612B (I_sipm and R measurement) and Keithley 2400 
    (I_led measurement). This function performs a voltage sweep on the sipm while
    measuring I, with led polarized with a fixed current. Format of iv data is 
    I_led, V_sipm, I_sipm. Data format of r data is R_rtd, I_rtd.
    
    ---------
    
    """
    ######---------- Set R gap for measurment -----------------######
    
    readingsI_led = []
    readingsV_led = []
    readingsI_sipm = []
    readingsR = []
    tiempo = []
    
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
         
    
    #---------------------------------------------------------------------------
    
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
    smu_2612b.write('display.smub.measure.func = display.MEASURE_DCVOLTS')
    
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


    print("Measuring temperature")        
        
    condition = thermostatInitial(smu_2612b, tolerance)

    print("Temperature: " + str(condition - tolerance) + " \pm " + str(tolerance))

    print("Start of measurement")
    if return_sweep == 1:
        print("Return active")
    smu_2612b.write('smub.source.output = smub.OUTPUT_ON')
    smu_2612b.write('smua.source.output = smua.OUTPUT_ON')
    smu_2400.write('OUTP ON')
    smu_2612b.write('smub.source.leveli = ' + '0')
    
    i = iStart
    while (i <= iEnd):
        
        smu_2612b.write('smua.measure.r(smua.nvbuffer1)')
        R_condition = cast(readBuffer(smu_2612b, 'a')[0])
        
        temp = []
        
        if R_condition[-1] < (condition + tolerance) and R_condition[-1] > (condition - tolerance):
            print(i)

            smu_2612b.write('smub.source.leveli = ' + str(i))
            time.sleep(wait_time)
            smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
            smu_2612b.write('smua.measure.r(smua.nvbuffer1)')
            
            auxRead = smu_2400.query(':READ?')
            sipm_current = float(cast(auxRead)[1])
            
            smu_2612b.write('smub.source.leveli = ' + '0')
            
            readingsR_temp = readBuffer(smu_2612b, 'a')[0]
            temp = cast(readingsR_temp)
            readingsR.append(temp[-1])
            tiempo.append(time.time())
            
            
            readingsI_sipm.append(sipm_current)
            
            i += iStep
                
            #smu_2612b.write('smua.nvbuffer1.clear()')
        elif R_condition[-1] < (condition - tolerance):
            smu_2612b.write('smub.source.leveli = ' + '0.080')
            time.sleep(1)
            smu_2612b.write('smub.source.leveli = ' + '0')
        else:
            time.sleep(3)
            
    i -= iStep
    
    if return_sweep == 1:
        
        while (i >= iStart):
            smu_2612b.write('smua.measure.r(smua.nvbuffer1)')
            R_condition = cast(readBuffer(smu_2612b, 'a')[0])
              
            temp = []
            
            if R_condition[-1] < (condition + tolerance) and R_condition[-1] > (condition - tolerance):
                print(i)
                    
                smu_2612b.write('smub.source.leveli = ' + str(i))
                time.sleep(wait_time)
                smu_2612b.write('smub.measure.v(smub.nvbuffer1)')
                smu_2612b.write('smua.measure.r(smua.nvbuffer1)')
                
                auxRead = smu_2400.query(':READ?')
                sipm_current = float(cast(auxRead)[1])
                
                smu_2612b.write('smub.source.leveli = ' + '0')
                
                readingsR_temp = readBuffer(smu_2612b, 'a')[0]
                temp = cast(readingsR_temp)
                readingsR.append(temp[-1])
                tiempo.append(time.time())
            
                readingsI_sipm.append(sipm_current)
            
                i -= iStep
            
            elif R_condition[-1] < (condition - tolerance):
                smu_2612b.write('smub.source.leveli = ' + '0.140')
                time.sleep(1)
                smu_2612b.write('smub.source.leveli = ' + '0')    
            else:
                time.sleep(3)
                
            
    smu_2612b.write('smua.source.output = smua.OUTPUT_OFF')
    smu_2612b.write('smub.source.output = smub.OUTPUT_OFF')
    smu_2400.write('OUTP OFF')
    
    print("End of measurement")
    
    readingsI_led_temp = readBuffer(smu_2612b, 'b')[1]
    readingsV_led_temp = readBuffer(smu_2612b, 'b')[0]
    
    readingsI_led = cast(readingsI_led_temp)
    readingsV_led = cast(readingsV_led_temp)

    return [readingsI_sipm, readingsV_led, readingsI_led, readingsR]
