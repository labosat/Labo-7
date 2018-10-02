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
    
    i_ccb          = 18*P('m')
    v_ccb          = 30
    
    iRangb         = 'AUTO'
    vRangb         = 200
    
    source         = 'V'        #source function for smub ('iv') measurement
   
    vStart         = 22.75
    vEnd           = 25
    vStep          = 10*P('m')
    
    # -------------------------------------------------------------------------
    #I sweep used for led in 'led' mode and for sipm in 'iv' mode -------------
    
    iStart         = 0
    iEnd           = 5*P('u')
    iStep          = 50*P('n')
    
    # -------------------------------------------------------------------------
    # for led only ------------------------------------------------
    
    v_cc_led       = 1
    
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
            NPLC]