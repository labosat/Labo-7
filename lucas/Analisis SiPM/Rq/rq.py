import numpy as np
import os
from functions import tolerance, dispersion, weightedMean, error_R

os.chdir("C:/Users/lucas/Documents/GitHub/Labo-7/lucas/Analisis SiPM/Rq/")


base_path = "measurements/"
array = []
R_out = []
R_out_err = []

i = 1
while True:
    path = base_path + "Estacionario " + str(i)
    if os.path.exists(path):
        j = 1
        try:
            array.append(tolerance(0.03, path))
            
            data = np.loadtxt(path + "/res/" + str(j) + " (res).txt", skiprows=1)
            R = data[:, 1]
            R_err_syst = error_R(R)
            R_err_stat = dispersion(R)/np.sqrt(len(R)) 

            R_err = np.sqrt(R_err_stat**2 +  R_err_syst**2)
            
            R_out.append(weightedMean(R, R_err))
            
            #systematic error. Is mean ok here?
            R_out_err.append(np.mean(R_err))
        
            j += 1
        except IOError:
            break
        
        i += 1
    else:
        break


for k in range(1, len(array) + 1):
    np.savetxt('arrays/array %s.txt' % k, np.c_[array[k - 1]])
    
np.savetxt('arrays/R.txt', np.c_[R_out])
np.savetxt('arrays/R_err.txt', np.c_[R_out_err])

#np.savetxt('arrays/R.txt', np.c_[R_out, R_out_err])
