import visa
from functions import cast, readBuffer, error_V, error_I

class smu2612b:
    
    def __init__(self, address):
        rm = visa.ResourceManager()
        equipment_id = 'GPIB0::' + str(address) + '::INSTR'
    
        self.smu = rm.open_resource(equipment_id)
        self.name = "SMU2612B"
        
        self.smu.write('smua.reset()')
        self.smu.write('smub.reset()')
        self.smu.write('reset()')
        
        self.smu.write('format.data = format.ASCII')
        
        # Buffer operations -------------------------------------------------------
        
        self.smu.write('smua.nvbuffer1.clear()')
        self.smu.write('smub.nvbuffer1.clear()')
        
        self.smu.write('smua.nvbuffer1.appendmode = 1')
        self.smu.write('smub.nvbuffer1.appendmode = 1')
        
        self.smu.write('smua.nvbuffer1.collectsourcevalues = 1')
        self.smu.write('smub.nvbuffer1.collectsourcevalues = 1')
    
        self.smu.write('smua.measure.count = 1')
        self.smu.write('smub.measure.count = 1')
        
        return
    
    def setup(self, config):
        
        [enable_a,
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
         delay_b] = config
        
        
        if enable_a == 1:
            if source_a == 'V' and measure_a == 'I':
                self.measure_a = 'I'
                
                # -------------------------------------------------------------------------   
                # smua configuration
                
                self.smu.write('smua.source.func = smua.OUTPUT_DCVOLTS')
                self.smu.write('smua.measure.func = smua.OUTPUT_DCAMPS')
                self.smu.write('display.smua.measure.func = display.MEASURE_DCAMPS')
                
                if (measure_a_rang == 'AUTO'):
                   self.smu.write('smua.source.autorangei = smua.AUTORANGE_ON')
                else:
                    self.smu.write('smua.source.rangei = ' + str(measure_a_rang))
                
                if (source_a_rang == 'AUTO'):
                    self.smu.write('smua.measure.autorangev = smua.AUTORANGE_ON')
                else:
                    self.smu.write('smua.measure.rangev = ' + str(source_a_rang))
            
                #compliance values for I and V
                self.smu.write('smua.source.limiti = ' + str(measure_a_cc))
                self.smu.write('smua.source.limitv = ' + str(source_a_cc))
            	
                self.smu.write('smua.measure.nplc = ' + str(NPLC_a))
                self.smu.write('smua.measure.delay = ' + str(delay_a))
                
            else:
                print("source/measure quantity invalid.")
                
        else:
            print("Channel a not enabled.")

        
        if enable_b == 1:
            if source_b == 'I' and measure_b == 'V':
                self.measure_b = 'V'
                
                # -------------------------------------------------------------------------   
                # smua configuration
                
                self.smu.write('smub.source.func = smub.OUTPUT_DCAMPS')
                self.smu.write('smub.measure.func = smub.OUTPUT_DCVOLTS')
                self.smu.write('display.smub.measure.func = display.MEASURE_DCVOLTS')
                
                if (measure_b_rang == 'AUTO'):
                   self.smu.write('smub.source.autorangei = smub.AUTORANGE_ON')
                else:
                    self.smu.write('smub.source.rangei = ' + str(measure_b_rang))
                
                if (source_b_rang == 'AUTO'):
                    self.smu.write('smub.measure.autorangev = smub.AUTORANGE_ON')
                else:
                    self.smu.write('smub.measure.rangev = ' + str(source_b_rang))
            
                #compliance values for I and V
                self.smu.write('smub.source.limiti = ' + str(measure_b_cc))
                self.smu.write('smub.source.limitv = ' + str(source_b_cc))
            	
                self.smu.write('smub.measure.nplc = ' + str(NPLC_b))
                self.smu.write('smub.measure.delay = ' + str(delay_b))
                
            else:
                print("source/measure quantity invalid.")
                
        else:
            print("Channel b not enabled.")
            
    def measure(self, channel, option=True):
        if channel == 'a':
            measure_func = self.measure_a
        elif channel == 'b':
            measure_func = self.measure_b
                
        self.smu.write('smu%s.source.output = smu%s.OUTPUT_ON' % (str(channel), str(channel)))
        
        if measure_func == 'I':
            self.smu.write('smu%s.measure.i(smu%s.nvbuffer1)' % (str(channel), str(channel)))
        elif measure_func == 'V':
            self.smu.write('smu%s.measure.v(smu%s.nvbuffer1)' % (str(channel), str(channel)))
        else:
            print("Invalid SMU channel")
            
        if option:
            self.smu.write('smu%s.source.output = smu%s.OUTPUT_OFF' % (str(channel), str(channel)))
        return


class smu2400:
    
    def __init__(self, address):
        rm = visa.ResourceManager()
        equipment_id = 'GPIB0::' + str(address) + '::INSTR'
    
        self.smu = rm.open_resource(equipment_id)
        self.name = "SMU2400"
        
        self.smu.write("*RST")
        
        return
    
    
class Experiment:
    
    def __init__(self, v, instrument_setup, experiment_setup):
        self.instruments = []
        for i in range(len(v)):
            self.instruments.append(v)
            
        for i in range(len(self.instruments)):
            print("Instruments in experiment:")
            print("%s. %s" % (i, self.instruments[i].name))
            self.instruments[i].setup(instrument_setup[i])
            
        self.experiment_setup = experiment_setup
        return
    
    def iv_curve(self, channel):
        
        """
        
        Function to perform iv curve with smu2612b
        
        """
        [start, end, step] = self.experiment_setup
        output_flag = False
        
        if channel == 'a':
            source_func = self.instruments[0].measure_a
        elif channel == 'b':
            source_func = self.instruments[0].measure_b
         
        j = start
        while j <= end:
            if source_func == 'V':
                self.instruments[0].smu.write('smu%s.source.levelv = %s' % (str(channel), str(j)))
            elif source_func == 'I':
                self.instruments[0].smu.write('smu%s.source.leveli = %s' % (str(channel), str(j))) 
                
            self.instruments[0].smu.measure(channel, output_flag)
            j += step
        
        if not output_flag:
            self.instruments[0].smu.write('smu%s.source.output = smu%s.OUTPUT_OFF' % (str(channel), str(channel)))
        
        readings_measure = cast(readBuffer(self.instruments[0].smu, str(channel))[1])
        readings_source = cast(readBuffer(self.instruments[0].smu, str(channel))[0])
         
        readings_source_error = error_V(readings_source, '2612')
        readings_measure_error = error_I(readings_measure, '2612')
         
        import matplotlib.pyplot as plt
        plt.errorbar(readings_source, readings_measure, 
                     xerr=readings_source_error, yerr=readings_measure_error, fmt='.')
        
        return [readings_source, readings_measure, readings_source_error, readings_measure_error]
    
    
    
    
