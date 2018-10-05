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
    
    i_ccb          = 155*P('m')
    v_ccb          = 3
    
    iRangb         = 'AUTO'
    vRangb         = 'AUTO'
    
    source         = 'I'        #source function for smub ('iv') measurement
   
    vStart         = 22.75
    vEnd           = 25
    vStep          = 10*P('m')
    
    # -------------------------------------------------------------------------
    #I sweep used for led in 'led' mode and for sipm in 'iv' mode -------------
    
    iStart         = 0*P('m')
    iEnd           = 190*P('m')
    iStep          = 2*P('m')
    
    # -------------------------------------------------------------------------
    # for led only ------------------------------------------------------------
    
    v_cc_led       = 3
    
    # -------------------------------------------------------------------------
    # return sweep on led tests -----------------------------------------------
    
    return_sweep   = 1
    
    # -------------------------------------------------------------------------
    # miscellaneous -----------------------------------------------------------

    NPLC           = 1        #integration time for k2612b (default = 1, higher for better accuracy)
   
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
            return_sweep]