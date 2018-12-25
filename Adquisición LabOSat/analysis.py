import numpy as np
import os
from functions import tolerance, dispersion, weightedMean, error_R, error_V, error_I, Linear, ClosestToOne
from scipy.odr import ODR, Model, RealData

pixels = 18980
m = 3.81

mode = 'rq'
encapsulado = 1

#tolerance in temperature
tol = 0.03


base_path = "results\\Encapsulado %s\\" % encapsulado
array = []
T = []
T_err = []
Rq = []
Rq_err = []

i = 1
while True:
    path = base_path + str(i) + " " + str(mode) + "\\"
    if os.path.exists(path):
        j = 1
        try:
            array.append(tolerance(tol, path))
            
            data = np.loadtxt(path + str(j) + ".txt", skiprows=1)
            T_temp = data[:, 2]
            T_err_syst = error_R(T_temp)
            T_err_stat = dispersion(T_temp)/np.sqrt(len(T_temp)) 

            T_err = np.sqrt(T_err_stat**2 + T_err_syst**2)
            
            T.append((weightedMean(T_temp, T_err) - 1000)/m)
            
            #systematic error. Is mean ok here?
            T_err.append(np.mean(T_err)/m)
        
            j += 1
        except IOError:
            break
        
        i += 1
    else:
        break

if mode == 'rq':

    for l in range(len(array)):
        Rq_temp = []
        Rq_err_temp = []
        #chi2_out = []
        for k in range(len(array[l])):
            path = base_path + str(l) + " " + str(mode) + "\\" + str(k) + ".txt"
            data = np.loadtxt(path + str(l) + ".txt", skiprows=1)
            V_temp = data[:, 0]
            I_temp = data[:, 1]
            V_err_temp = error_V(V_temp, '2612B')
            I_err_temp = error_I(I_temp, '2612B')
            
            chi2 = []
            slope = []
            for h in range(0, len(V_temp) - 2):
                V_temp = V_temp[h:]
                I_temp = I_temp[h:]
                V_err_temp = V_err_temp[h:]
                I_err_temp = I_err_temp[h:]
    
                linear_model = Model(Linear)
                data = RealData(V_temp, I_temp, sx=V_err_temp, sy=I_err_temp)
                odr = ODR(data, linear_model, beta0=[0., 1.])
                out = odr.run()
                
                m_temp = out.beta[0]
                m_err_temp = out.sd_beta[0]
                
                slope.append(m_temp)
                chi2.append(out.res_var)
                Rq_err_temp.append((pixels/m_temp**2) * m_err_temp)
            
            index = ClosestToOne(chi2)
            Rq.append(pixels/slope[index])
            #chi2_out.append(chi2[index])
            Rq_err.append(Rq_err_temp[index])
            
        value1 = np.sum(Rq_temp)
        #check this
        value2 = np.sum(Rq_err_temp)
        Rq.append(value1)
        Rq_err.append(value2)
        
    np.savetxt("rq_out, encapsulado %s.txt" % encapsulado, np.c_[T, T_err, Rq, Rq_err])
    import matplotlib.pyplot as plt
    
    plt.errorbar(T, Rq, xerr=T_err, yerr=Rq_err, fmt='.k', capsize=3)
    

elif mode == 'vbr':
    
    print("")
    
    
    
    

else:
    print("%s is not a valid mode" % mode)
    

