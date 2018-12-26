def setup():
    from functions import P
    
    # -------------------------------------------------------------------------
    # Modifiable values 
    # -------------------------------------------------------------------------
   
    # -------------------------------------------------------------------------
    # i_SIPM measurement ------------------------------------------------------
    
    i_cc_sipm      = 20*P('m')
    v_cc_sipm      = 31.5
    
    i_rang_sipm    = 'AUTO'
    v_rang_sipm    = 'AUTO'
    
    v_level_sipm   = 0
    
    # -------------------------------------------------------------------------
    # i_LED measurement -------------------------------------------------------
    
    i_cc_led       = 20*P('m')
    v_cc_led       = 3
    
    i_rang_led     = 'AUTO'
    v_rang_led     = 'AUTO'
   
	# -------------------------------------------------------------------------
	# sweep setup -------------------------------------------------------------
    
    start         = -1
    end           = 29
	
	# -------------------------------------------------------------------------
	# RTD measurement ---------------------------------------------------------
	
    fourWire	    = 1
	
    i_cc_rtd       = 300*P('u')
    v_cc_rtd       = 0.3
    
    i_rang_rtd     = 'AUTO'
    r_rang_rtd     = 2000
    
    i_level_rtd    = 97*P('u')
	
	# ------------------------------------------------------------------------- 
    
    return_sweep   = 0
	
    # number of measurements
    
    N			   = 3000

    points         = 100          # measurements per point in curve, 100 for NPLC = 1
	
    delay		   = 10*P('m')
    
    curves         = 1

   
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
        	start,
        	end,
        	fourWire,
        	i_cc_rtd,
        	v_cc_rtd,
        	i_rang_rtd,
        	r_rang_rtd, 
        	i_level_rtd,
        	return_sweep,
            N,
        	points,
        	delay,
            curves]