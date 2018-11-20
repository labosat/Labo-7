def setup():
    from functions import P
    
    # -------------------------------------------------------------------------
    # Modifiable values ('iv' test and 'led' test)
    # -------------------------------------------------------------------------
   
    #for smua only (r measurement) --------------------------------------------
    
    fourWire       = 1          # 1 for 4-wire sensing
    i_cca          = 300*P('u')
    v_cca          = 0.3
    
    iRanga         = 100*P('u')
    vRanga         = 0.2
    
    iLevela        = 97*P('u')
    
    # -------------------------------------------------------------------------
    #for smub only (iv curve measurement) -------------------------------------
    
    i_ccb          = 200*P('m')
    v_ccb          = 2
    
    iRangb         = 'AUTO'
    vRangb         = 'AUTO'
    
    source         = 'I'        #source function for smub ('iv' mode) measurement
   
    vStart         = 0
    vEnd           = 1
    vStep          = 100*P('m')
    
    # -------------------------------------------------------------------------
    # return sweep on 'led1' test -----------------------------------------------
    
    return_sweep   = 1
    
    # -------------------------------------------------------------------------
    #I sweep used for led in 'led' mode and for sipm in 'iv' mode -------------
    
    iStart         = 0*P('m')
    iEnd           = 20*P('m')
    iStep          = 25*P('u')
    
    # -------------------------------------------------------------------------
    # for led2 test only ------------------------------------------------------
    
    v_cc_led       = 2
    
    #wait_time functions as a "time step". Total time = measurements*wait_time
    measurements   = 100
    
    # -------------------------------------------------------------------------
    # miscellaneous -----------------------------------------------------------

    NPLC           = 1        #integration time for k2612b (0.01 - 25)
   
    # -------------------------------------------------------------------------
    # End of setup
    # -------------------------------------------------------------------------

    
    return [fourWire,
            i_cca,
            v_cca,
            iRanga,
            vRanga,
            iLevela,
            i_ccb,
            v_ccb,
            iRangb,
            vRangb,
            vStart,
            vEnd,
            vStep,
            iStart,
            iEnd,
            iStep,
            source,
            v_cc_led,
            NPLC,
            return_sweep,
            measurements]