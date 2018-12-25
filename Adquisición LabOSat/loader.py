import numpy as np
from functions import error_V, error_I

Encapsulado = 1
modo        = 'rq'

V_sipm      = []
I_sipm      = []
R           = []

i = 1
while True:
    try:
        path = '\\results\\Encapsulado %s\\%s (%s)\\' % (Encapsulado, i, modo)
        for i in range(len()):
            
        
        i += 1
    except IOError:
        break