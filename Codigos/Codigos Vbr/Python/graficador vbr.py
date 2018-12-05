import numpy as np
import matplotlib.pyplot as plt
import Funciones as f



I_dark = []
R = []
I_dark_err = []
R_err = []
for i in range(1, 20):
    path = '/home/tomas/Desktop/Labo 6 y 7/Labo-7/Mediciones/Vbr/Para informe/Vbr/Estacionario %s' % i
    array = f.pulidor(0.03, path)
    I_dark_temp = []
    R_temp = []
    I_dark_err_temp = []
    R_err_temp = []
    for j in array:
        dataR = np.loadtxt(path + '/res/%s (res).txt' % j, skiprows=1)
        data = np.loadtxt(path + '/iv/%s (iv).txt' %j)
        I_dark.append(data[:, 1][np.where(data[:, 0] == 30.)[0][0]])
        R.append(dataR[:, 1][np.where(data[:, 0] == 30.)[0][0]])
I_dark_err = f.error_I(I_dark, '2612')
R_err = f.error_R(R, 0.000097)

plt.errorbar(R, I_dark, xerr=R_err, yerr=I_dark_err, fmt='.k', capsize=3)
plt.grid(True)


def Linear(M, x):
    """
    Funcion lineal para ajustar con el ODR:
        
    >>> linear_model = Model(Linear)
    >>> data = RealData(X, Y, sx=X_err, sy=Y_err)
    >>> odr = ODR(data, linear_model, beta0=[0., 1.])
    >>> out = odr.run()
    
    >>> m = out.beta[0]
    >>> b = out.beta[1]
    >>> m_err = out.sd_beta[0]
    >>> b_err = out.sd_beta[1]        
    >>> chi2 = out.res_var
    .
    .
    """
    m, b = M
    return m*x + b

linear_model = Model(Linear)
data = RealData(T, vbr, sx=T_err, sy=vbr_err)
odr = ODR(data, linear_model, beta0=[0., 1.])
out = odr.run()
m = out.beta[0]
b = out.beta[1]

plt.errorbar(T, vbr, xerr=T_err, yerr=vbr_err, fmt = 'sk', capsize=3)
plt.grid(True)
plt.xlabel('Temperatura (C)', size=22)
plt.ylabel('Breakdown Voltage (V)', size=22)
plt.tick_params(labelsize=22)
plt.plot(T, [i*m + b for i in T], 'r-', lw = 2)


plt.plot(R, I_dark, '.')
plt.grid(True)
