from functions import P

def setup1():
   
    # -------------------------------------------------------------------------
    # Channel a: SIPM ---------------------------------------------------------
    
    enable_a         = 1
    
    source_a_cc      = 2*P('m')
    measure_a_cc     = 30
    
    source_a_rang    = 'AUTO'
    measure_a_rang   = 'AUTO'
    
    source_a         = 'V'
    measure_a        = 'I'
    
    NPLC_a           = 1
    delay_a          = 10*P('s')
    
    # -------------------------------------------------------------------------
    # Channel b: LED ----------------------------------------------------------
    
    enable_b         = 1
    
    source_b_cc      = 500*P('u')
    measure_b_cc     = 3
    
    source_b_rang    = 'AUTO'
    measure_b_rang   = 'AUTO'

    source_b         = 'I'
    measure_b        = 'V'
    
    NPLC_b           = 1
    delay_b          = 10*P('s')
  
    return [enable_a,
            source_a_cc,
            measure_a_cc,
            source_a_rang,
            measure_a_rang,
            source_a,
            measure_a,
            NPLC_a,
            delay_a,
            enable_b,
            source_b_cc,
            measure_b_cc,
            source_b_rang,
            measure_b_rang,
            source_b,
            measure_b,
            NPLC_b,
            delay_b]
    
def setup2():
	
    # -------------------------------------------------------------------------
	# RTD ---------------------------------------------------------------------    
    
    four_wire	   = 1
	
    source_cc      = 300*P('u')
    measure_cc     = 0.3
    
    source_rang    = 'AUTO'
    measure_rang   = 2000
    
    return [four_wire,
            source_cc,
            measure_cc,
            source_rang,
            measure_rang]
    
def experiment_setup():
	
#	# ------------------------------------------------------------------------- 
#    
#    return_sweep   = 1
#	
#    # number of measurements
#    
#    N			   = 135
#
#    points         = 16          # measurements per point in curve
#	
#    
#    curves         = 1
    
    source_start = 0
    source_end   = 1
    source_step  = 0.01 
    
    return [source_start, source_end, source_step]
    