import numpy as np
import matplotlib.pyplot as plt
import time
from SMU_2612B import smu2612b, error_I, error_V


NPLC = 1   
delay = 0.01

smua = smu2612b('a')
smua.ranges('autorange', 'autorange')
smua.NPLC(NPLC)
smua.compliance(0.7, 0.100)
smua.start_measurment()

time.sleep(1)        

#N = np.arange(-2, 6, 0.05)
N = []
for i in range(100):
    N.append(0)
    N.append(np.random.rand() + 5)
    
for current in N:
    smua.iv(current)
    
time.sleep((len(N) * NPLC) / 50. + len(N) * delay)

I, V = smua.end_measurment()
        
        
plt.plot(V, I, 'o')
   