import numpy as np
import matplotlib.pyplot as plt
import funcionesVbr as f
from scipy.optimize import curve_fit
from scipy.odr import Model, RealData, ODR
from funcionesVbr import vbr, Linear, exp, exp_inv

def Breakdown_Voltage(path, tolerancia):
    array = f.pulidor(tolerancia, path)
    celdas = 18980
    parameters = 2
    R = []
    R_err = []
    Rq = []
    Rq_err = []
    chi2_out = []
    Vbr = []
    parametro_2 = []
    Vbr_err = []
    parametro_2_err = []
    dark_current = []
    dark_current_err = []
    for h in array:
        data1 = np.loadtxt(path+'/res/%s (res).txt' % h, skiprows=1)
        Res = data1[:, 1]   
        I = data1[:, 2]
        V = I*Res
        V_err = V*0.00015 + 225E-6
        I_err = I*0.0003 + 60E-9
        Res_err_estadistico = f.dispersion(Res) 
        Res_err_sistematico = np.sqrt((1/I**2) * V_err**2 + ((V/(I**2))**2)*I_err**2)
        Res_err = np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico**2)
        R.append(f.weightedMean(Res, Res_err))
        R_err.append(f.weightedError(Res, Res_err))
        
        data2 = np.loadtxt(path+'/iv/%s (iv).txt' % h, skiprows=1)
        V = data2[:, 0]
        I = data2[:, 1]

        
        ranges = f.DetermineRange(V, I)
        V_err = f.SourceError(V, 'V', ranges[0])
        I_err = f.MeasureError(I, 'I', '10uA')
        
        H = list(V)
        dark_index = H.index(30.0)
        dark_current.append(I[dark_index])
        dark_current_err.append(I_err[dark_index])
                
#        
#  #      #reverse data:
# #       #V = [V[len(V)-i-1] for i in range(len(V))]
##        #I = [I[len(I)-i-1] for i in range(len(I))]
#
#        
#        I = [np.log(i) for i in I]
#        I_err = [abs((1/I[i])*I_err[i]) for i in range(len(I))]
#        
#        V, V_err, I, I_err = f.DerivateData(V, V_err, I, I_err)
#            
    
       # #degree = 0
      #  #V, V_err, I, I_err = f.Smooth(V, V_err, I, I_err, 1)
        
#        
#      #  DESBLOQUEAR SOLO SI SE QUIERE USAR EL SMOOTHING DE PYTHON.
#     #   from scipy.signal import savgol_filter
#    #    yhat = savgol_filter(I, 51, 3)
#   #     #plt.figure(2)
#  #      #plt.plot(V, yhat, '.')
# #       yhat = list(yhat)
##        index_max = yhat.index(max(yhat))
##        I = yhat
        
#        index_max = I.index(max(I))
#        I = [I[i] for i in range(index_max, len(I))]
#        V = [V[i] for i in range(index_max, len(V))]
#        V_err = [V_err[i] for i in range(index_max, len(V_err))]
#        I_err = [I_err[i] for i in range(index_max, len(I_err))]
#        
#        chi2 = []
#        N = len(I)
#        for j in range(N-2):
#            I_temp = [I[i] for i in range(N-j)]
#            I_temp = np.asarray(I_temp)
#            V_temp = [V[i] for i in range(N-j)]
#            V_temp = np.asarray(V_temp)
#            V_err_temp = [V_err[i] for i in range(N-j)]
#            V_err_temp = np.asarray(V_err_temp)
#            I_err_temp = [I_err[i] for i in range(N-j)]
#            I_err_temp = np.asarray(I_err_temp)
#    #        fit, _ = curve_fit(f.vbr, V_temp, I_temp, sigma=I_err_temp)
#    #        chi2.append(chisq/(len(I_temp)-2))
#            
#            exp_model = Model(vbr)
#            data = RealData(V_temp, I_temp, sx=V_err_temp, sy=I_err_temp)
#            odr = ODR(data, exp_model, beta0=[0., 1.])
#            out = odr.run()
#            a_temp = out.beta[0]
#            b_temp = out.beta[1]
#            a_err_temp = out.sd_beta[0]
#            chi2.append(out.res_var)
#            
#        I_fit = [I[i] for i in range(N-f.ClosestToOne(chi2))]
#        V_fit = [V[i] for i in range(N-f.ClosestToOne(chi2))]
#        V_err_fit = [V_err[i] for i in range(N-f.ClosestToOne(chi2))]
#        I_err_fit = [I_err[i] for i in range(N-f.ClosestToOne(chi2))]
#        exp_model = Model(vbr)
#        data = RealData(V_fit, I_fit, sx=V_err_fit, sy=I_err_fit)
#        odr = ODR(data, exp_model, beta0=[0., 1.])
#        out = odr.run()
#        a_temp = out.beta[0]
#        b_temp = out.beta[1]
#        a_err_temp = out.sd_beta[0]    
#        b_err_temp = out.sd_beta[1]    
    
##        plt.figure(2)
##        plt.plot(V_fit, I_fit, '.')
#        #degree = 0
#        #V, V_err, I, I_err = f.Smooth(V, V_err, I, I_err, 1)
#        
#        Vbr.append(b_temp)
#        parametro_2.append(a_temp)
#        Vbr_err.append(a_err_temp)
#        parametro_2_err.append(b_err_temp)
    
#    return R, R_err, Vbr, parametro_2, Vbr_err, parametro_2_err, dark_current, array
    return R, R_err, dark_current, dark_current_err, array
#%%
#R, R_err, Vbr, parametro_2, Vbr_err, parametro_2_err, dark_current, array = Breakdown_Voltage(path, 0.03)

# Grafico a presentar: promedio de los clusters vs T
#
path_grupos = '/home/labosat/Desktop/Finazzi-Ferreira/Labo7/Vbr en T/results/'
R_totals = []
R_promedio = []
R_err_promedio = []
DC_totals = []
DC_totals_err = []
R_err_totals = []
numero_grupos = 19
for i in range(1, numero_grupos):
    R, R_err, dark_current, dark_current_err, array = Breakdown_Voltage(path_grupos + 'Estacionario %s' % i, 0.02)
    R_totals.append(R)
    DC_totals.append(f.weightedMean(dark_current, dark_current_err))
    DC_totals_err.append(f.weightedError(dark_current, dark_current_err))
    R_err_totals.append(R_err)
    R_promedio.append(f.weightedMean(R, R_err))
    R_err_promedio.append(f.weightedErrorR(R, R_err))
#    np.savetxt('array %s.txt' % i, array)
#
#np.savetxt('R.txt', R_promedio)
#np.savetxt('Rerr.txt', R_err_promedio)

    


T = [(R_promedio[i]-1000)/3.815 for i in range(len(R_promedio))]
T_err = [R_err_promedio[i]/3.815 for i in range(len(R_err_promedio))]

plt.figure(1)
#plt.plot(T, DC_total, '.')
plt.errorbar(T, DC_totals, yerr=DC_totals_err, xerr=T_err, fmt='.')
plt.yscale('log')
plt.xlabel('Temperatura (C)')
plt.ylabel('Dark Current')





#%%
# Fitteamos la corriente oscura en escala logaritmica por una funcion 
# lineal.    

linear_model = Model(Linear)
data = RealData(T, np.log(DC_totals), sx=T_err, sy=[DC_totals_err[i]/DC_totals[i] for i in range(len(DC_totals))])
odr = ODR(data, linear_model, beta0=[0., 1.])
out = odr.run()

m_temp = out.beta[0]
b_temp = out.beta[1]
m_err_temp = out.sd_beta[0]
chi2 = out.res_var

plt.figure(2)
plt.plot(T, [(m_temp*T[i] + b_temp) for i in range(len(T))])
plt.errorbar(T, np.log(DC_totals), yerr=[DC_totals_err[j]/DC_totals[j] for j in range(len(DC_totals))], xerr=T_err, fmt='.')
plt.xlabel('Temperatura (C)')
plt.ylabel('log Dark Current')
#%%
#Fitteamos la corriente oscura por una exponencial

path_grupos = '/home/labosat/Desktop/Finazzi-Ferreira/Labo7/Vbr en T/results/'
R_totals = []
DC_totals = []
DC_totals_err = []
R_err_totals = []
numero_grupos = 19
for i in range(1, numero_grupos):
    R, R_err, dark_current, dark_current_err, array = Breakdown_Voltage(path_grupos + 'Estacionario %s' % i, 0.02)
    R_totals.append(R)
    DC_totals.append(dark_current)
    DC_totals_err.append(dark_current_err)
    R_err_totals.append(R_err)

R_total = [item for sublist in R_totals for item in sublist]
DC_total = [item for sublist in DC_totals for item in sublist]
R_err_total = [item for sublist in R_err_totals for item in sublist]
DC_total_err = [item for sublist in DC_totals_err for item in sublist]


T = [(R_promedio[i]-1000)/3.815 for i in range(len(R_promedio))]
T_err = [R_err_promedio[i]/3.815 for i in range(len(R_err_promedio))]


exp_model = Model(exp_inv)
data = RealData(T, DC_totals, sx=T_err, sy=DC_totals_err)
odr = ODR(data, exp_model, beta0=[10000., 1000000., 0.1])
out = odr.run()

a_temp = out.beta[0]
b_temp = out.beta[1]
c_temp = out.beta[2]
m_err_temp = out.sd_beta[0]
chi2 = out.res_var

plt.figure(3)
plt.plot(np.arange(-35, 36, 0.05), [(a_temp * np.exp(b_temp * np.arange(-35, 36, 0.05)[i])) for i in range(len(np.arange(-35, 36, 0.05)))])
plt.errorbar(T, DC_totals, yerr=DC_totals_err, xerr=T_err, fmt='.')
plt.grid(True)
#plt.yscale('log')
plt.xlabel('Temperatura (C)')
plt.ylabel('Dark Current')


