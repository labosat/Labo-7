def setup():
    from functions import P
    
    # -------------------------------------------------------------------------
    # Modifiable values 
    # -------------------------------------------------------------------------
   
    # -------------------------------------------------------------------------
    # i_SIPM measurement ------------------------------------------------------
    
    i_cc_sipm      = 20*P('m')
    v_cc_sipm      = 31
    
    i_rang_sipm    = 'AUTO'
    v_rang_sipm    = 'AUTO'
    
    v_level_sipm   = 30
    
    # -------------------------------------------------------------------------
    # i_LED measurement -------------------------------------------------------
    
    i_cc_led       = 200*P('m')
    v_cc_led       = 2
    
    i_rang_led     = 'AUTO'
    v_rang_led     = 'AUTO'
   
    iStart         = 10*P('u')
    iEnd           = 20*P('m')
	
	 # -------------------------------------------------------------------------
	 # RTD measurement ---------------------------------------------------------
	
    fourWire	    = 1
	
    i_cc_rtd       = 300*P('u')
    v_cc_rtd       = 0.3
    
    i_rang_rtd     = 'AUTO'
    r_rang_rtd     = 2000
    
    i_level_rtd    = 97*P('u')
	
	# ------------------------------------------------------------------------- 
    
    return_sweep   = 1
	
    # number of measurements
    
    N			       = 40

    NPLC           = 0.16        #integration time for k2612b (0.01 - 25)
	
    delay		    = 5*P('m')

   
    # -------------------------------------------------------------------------
    # End of setup
    # -------------------------------------------------------------------------

    
    return [i_cc_sipm,
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
    			fourWire,
    			i_cc_rtd,
    			v_cc_rtd,
    			i_rang_rtd,
    			r_rang_rtd, 
    			i_level_rtd,
    			return_sweep,
            N,
    			NPLC,
    			delay]