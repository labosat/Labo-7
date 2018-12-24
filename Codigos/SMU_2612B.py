import visa

class SMU2612B:
    
    def __init__(self, channel, source):
        
        self.channel = channel
        self.source = source      # source = 'I'   or   source = 'V'
        self.NPLC = 1          #choose from 0.001 to 25
        self.delay = 0
        
        rm = visa.ResourceManager()
        equipment_id1 = 'GPIB0::' + str(26) + '::INSTR'
    
        self.smu_2612b = rm.open_resource(equipment_id1)
        
        self.smu_2612b.write('smu%s.reset()' % self.channel)
        self.smu_2612b.write('reset()')
        
        self.smu_2612b.write('format.data = format.ASCII')
        
        # Buffer operations -------------------------------------------------------
        
        self.smu_2612b.write('smu%s.nvbuffer1.clear()' % self.channel)
        
        self.smu_2612b.write('smu%s.nvbuffer1.appendmode = 1' % self.channel)
        
        self.smu_2612b.write('smu%s.nvbuffer1.collectsourcevalues = 1' % self.channel)
    
        self.smu_2612b.write('smu%s.measure.count = 1' % self.channel)
        
        self.smu_2612b.write('smu%s.measure.nplc = ' % self.channel + str(self.NPLC))
        
        self.smu_2612b.write('smu%s.measure.delay = ' % self.channel + str(self.delay))
                
    def ranges(self, set_v_range, set_i_range):
        
        ''' Sets the ranges. If the input is a number, it must be one of the possible ranges of the SMU.
            For autorange measurments the input must be 'autorange'. '''
        
        try:    # esto settea el rango de V 
            set_v_range = float(set_v_range)
            if self.source == 'V':
                self.smu_2612b.write('smu%s.source.rangev = ' % self.channel + str(set_v_range))
            else:
                self.smu_2612b.write('smu%s.measure.rangev = ' % self.channel + str(set_v_range))
        except ValueError:
            if self.source == 'V':
                self.smu_2612b.write('smu%s.source.autorangev = smu%s.AUTORANGE_ON' % (self.channel, self.channel))
            else:
                self.smu_2612b.write('smu%s.measure.autorangev = smu%s.AUTORANGE_ON' % (self.channel, self.channel))
                
        try:    # esto settea el rango de I
            set_v_range = float(set_i_range)
            if not self.source == 'V':
                self.smu_2612b.write('smu%s.source.rangei = ' % self.channel + str(set_v_range))
            else:
                self.smu_2612b.write('smu%s.measure.rangei = ' % self.channel + str(set_v_range))
        except ValueError:
            if not self.source == 'V':
                self.smu_2612b.write('smu%s.source.autorangei = smu%s.AUTORANGE_ON' % (self.channel, self.channel))
            else:
                self.smu_2612b.write('smu%s.measure.autorangei = smu%s.AUTORANGE_ON' % (self.channel, self.channel))


    def compliance(self, v_compliance, i_compliance):
        
        ''' Sets voltage and current compliance. '''
        
        self.smu_2612b.write('smu%s.source.limiti = ' % self.channel + str(i_compliance))
        self.smu_2612b.write('smu%s.source.limitv = ' % self.channel + str(v_compliance))
            
    def NPLC(self, NPLC):    #choose from 0.001 to 25
        
        ''' Sets the integration time of the SMU. '''
        
        self.smu_2612b.write('smu%s.measure.nplc = ' % self.channel + str(NPLC))
        
    def wait_time(self, wait_time):
        
        ''' Sets the delay between the source value is setted and the measurment is taken. '''
        
        self.smu_2612b.write('smu%s.measure.delay = ' % self.channel + str(wait_time))
        
        
    def start_measurment(self):
        
        ''' Prepares the SMU for measurments. Turns the output on and sets the source on voltage or current. '''
        
        if self.source == 'V':
            self.smu_2612b.write('smu%s.source.func = smu%s.OUTPUT_DCVOLTS' % (self.channel, self.channel))
            self.smu_2612b.write('display.smu%s.measure.func = display.MEASURE_DCAMPS' % self.channel)
            
        else:
            self.smu_2612b.write('smu%s.source.func = smu%s.OUTPUT_DCAMPS' % (self.channel, self.channel))
            self.smu_2612b.write('display.smu%s.measure.func = display.MEASURE_DCVOLTS' % self.channel)
            
        self.smu_2612b.write('smu%s.source.output = smu%s.OUTPUT_ON' % (self.channel, self.channel))         
        
    def iv(self, source_value):
        
        '''Measures an I-V value. First it stablish the source value, then takes the measurment. '''
        
        if self.source == 'V':
            self.smu_2612b.write('smu%s.source.levelv = ' % self.channel + str(source_value))
            self.smu_2612b.write('smu%s.measure.i(smu%s.nvbuffer1)' % (self.channel, self.channel))

        else:
            self.smu_2612b.write('smu%s.source.leveli = ' % self.channel + str(source_value))
            self.smu_2612b.write('smu%s.measure.v(smu%s.nvbuffer1)' % (self.channel, self.channel))
        
    def res(self, source_value, voltage_source = True, four_wire = True):
        
        if four_wire:
            self.smu_2612b.write('smu%s.sense = smu%s.SENSE_REMOTE' % (self.channel, self.channel))
        
        elif not four_wire:
            self.smu_2612b.write('smu%s.sense = smu%s.SENSE_LOCAL' % (self.channel, self.channel))
        
        if not self.source == 'V':
            self.smu_2612b.write('smu%s.source.leveli = ' % self.channel + str(source_value))
            
        elif self.source == 'V':
            self.smu_2612b.write('smu%s.source.levelv = ' % self.channel + str(source_value))
        
        self.smu_2612b.write('smu%s.measure.r(smu%s.nvbuffer1)' % (self.channel, self.channel))
        
    def decoder(self, string):
        
        ''' Decodes the buffers measurments into readible values. '''
        
        out = []
        for values in string.split(','):
            aux = values
            out.append(float(aux))
      
        return out    
    
    def wait_complete(self):

       ''' Hardware wait time to finish the measurment. '''    
        
       self.smu_2612b.write('waitcomplete()')
        
            
    def end_measurment(self):
        
        ''' End the measurment after hole curve. Turns off the output, request the measurments from the 
            buffer and gives it as readible values. '''
        
        self.smu_2612b.write('smu%s.source.output = smu%s.OUTPUT_OFF' % (self.channel, self.channel))
        
        measure_temp = self.smu_2612b.query('printbuffer(1, smu%s.nvbuffer1.n, smu%s.nvbuffer1.readings)' % (self.channel, self.channel))
        source_temp = self.smu_2612b.query('printbuffer(1, smu%s.nvbuffer1.n, smu%s.nvbuffer1.sourcevalues)' % (self.channel, self.channel))
        
        measure = self.decoder(measure_temp)
        source = self.decoder(source_temp)
        
        return measure, source


def error_I(y, SMU, source = False):
    """
    Esta funcion esta diseñada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonces
    I_led_temp_1 = I_led[1:int(len(I_led)/2)]es la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    if SMU == '2612':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.0003
                    offset = 800*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.0003
                    offset = 5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0003
                    offset = 60*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0003
                    offset = 300*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0003
                    offset = 6*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0003
                    offset = 30*pow(10, -6)                
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0005
                    offset = 1.8*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <= 1.5: 
                    percentage = 0.0006
                    offset = 4*pow(10, -3)
                else:
                    percentage = 0.005
                    offset = 40*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00025
                    offset = 500*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.00025
                    offset = 1.5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0002
                    offset = 25*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0002
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0002
                    offset = 2.5*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0002
                    offset = 20*pow(10, -6)                
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0003
                    offset = 1.5*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <=1.5: 
                    percentage = 0.0005
                    offset = 3.5*pow(10, -3)
                else:
                    percentage = 0.004
                    offset = 25*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00029
                    offset = 300*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00027
                    offset = 700*pow(10, -12)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00025
                    offset = 6*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00027
                    offset = 60*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00035
                    offset = 600*pow(10, -9)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00055
                    offset = 6*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0022
                    offset = 570*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00035
                    offset = 600*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00033
                    offset = 2*pow(10, -9)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00031
                    offset = 20*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00034
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00045
                    offset = 2*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00066
                    offset = 20*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0027
                    offset = 900*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')        
    
    return temp


def error_V(x, SMU, source = True):
    """
    Esta funcion esta diseñada para crear un array con los errores del voltaje 
    medido o sourceado por un Kiethley 2611B, 2612B, 2614B.
    La función toma una lista que tiene el voltaje, y un boolean que indica si el 
    mismo fue medido o sourceado.
    
    Input: (V, source = True)
    
    Si no se especifica el source, entonces el voltaje fue sourceado. Si source = False,
    entonces se midio voltaje.
    
    Returns:  V_err  (list)
    .
    .
    """
    if SMU == '2612':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 375*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00015
                    offset = 225*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 350*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 600*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 2.4*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 24*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00012
                    offset = 300*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.00012
                    offset = 300*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 1.5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 10*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
        
    return temp    


#%%
import numpy as np
import matplotlib.pyplot as plt
import time

source = 'V'
smua = SMU2612B('a', source)
smua.ranges('autorange', 'autorange')
smua.NPLC = 1
smua.delay = 0
smua.compliance(2, 0.100)
smua.start_measurment()

time.sleep(2)        

N = np.arange(-2, 2, 0.1)
for i in N:
    smua.iv(i)
#N = 100
#for current in range(N):
#    smua.res(0.0001, voltage_source=False, four_wire=False)

smua.wait_complete()
    
time.sleep((len(N) * smua.NPLC) / 50. + len(N) * smua.delay)

I, V = smua.end_measurment()
        
        
plt.plot(V, I, 'o')