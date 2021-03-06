import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from Funciones import Linear
import sys
sys.path.append('./Labo-7/')
from scipy.odr import Model, RealData, ODR

path = 'C:/Users/LINE/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Integration Time'

I = []
V = []
I_err = []
V_err = []
for i in np.arange(0, 30, 5):
        data = np.loadtxt(path + '/Integration %s/iv/1 (iv).txt' % i, skiprows=1)
        I.append(data[:, 1])
        V.append(data[:, 0])        
        I_err.append(f.error_I(data[:, 1]))
        V_err.append(f.error_V(data[:, 0]))

def sigma(X, Y, X_err, Y_err):
    linear_model = Model(Linear)
    data = RealData(X, Y, sx=X_err, sy=Y_err)
    odr = ODR(data, linear_model, beta0=[0., 1.])
    out = odr.run()
    
    m = out.beta[0]
    b = out.beta[1]
    recta = [(I[i] - (V[i]*m+b)) for i in range(len(I))]
    return len(recta), f.dispersion(recta)
    
sigmas = []
g, ([ax1, ax2, ax3], [ax4, ax5, ax6]) = plt.subplots(2, 3)
g.tight_layout()
ax1.plot(V[0][:55], I[0][:55], '.')
a = sigma(V[0][:55], I[0][:55], V_err[0][:55], I_err[0][:55])[1]
sigmas.append(a)
#ax1.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax1.set_title('Integration time = 1', fontsize=18)
ax1.set_xlabel('V', fontsize=15)
ax1.set_ylabel('I (A)', fontsize=15)
ax1.grid(True)
ax2.plot(V[1][:55], I[1][:55], '.')
a = sigma(V[1][:55], I[1][:55], V_err[1][:55], I_err[1][:55])[1]
sigmas.append(a)
#ax2.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax2.set_xlabel('V', fontsize = 15)
ax2.set_ylabel('I (A)', fontsize = 15)
ax2.set_title('Integration time = 5', fontsize=18)
ax2.grid(True)
ax3.plot(V[2][:55], I[2][:55], '.')
a = sigma(V[2][:55], I[2][:55], V_err[2][:55], I_err[2][:55])[1]
sigmas.append(a)
#ax3.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax3.set_xlabel('V', fontsize = 15)
ax3.set_ylabel('I (A)', fontsize = 15)
ax3.set_title('Integration time = 10', fontsize=18)
ax3.grid(True)
ax4.plot(V[3][:55], I[3][:55], '.')
a = sigma(V[3][:55], I[3][:55], V_err[3][:55], I_err[3][:55])[1]
sigmas.append(a)
#ax4.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax4.set_xlabel('V', fontsize = 15)
ax4.set_ylabel('I (A)', fontsize = 15)
ax4.set_title('Integration time = 15', fontsize=18)
ax4.grid(True)
ax5.plot(V[4][:55], I[4][:55], '.')
a = sigma(V[4][:55], I[4][:55], V_err[4][:55], I_err[4][:55])[1]
sigmas.append(a)
#ax5.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax5.set_xlabel('V', fontsize = 15)
ax5.set_ylabel('I (A)', fontsize = 15)
ax5.set_title('Integration time = 20', fontsize=18)
ax5.grid(True)
ax6.plot(V[5][:55], I[5][:55], '.')
a = sigma(V[5][:55], I[5][:55], V_err[5][:55], I_err[5][:55])[1]
sigmas.append(a)
#ax6.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax6.set_xlabel('V', fontsize = 15)
ax6.set_ylabel('I (A)', fontsize = 15)
ax6.set_title('Integration time = 25', fontsize=18)
ax6.grid(True)


plt.figure(2)
plt.plot([1, 5, 10, 15, 20, 25], sigmas, 'o')
plt.xlabel('Integration time')
plt.ylabel('Dispersion')
plt.grid(True)

n, sigma = sigma(V[5][:55], I[5][:55], V_err[5][:55], I_err[5][:55])
error_sigmas = [(2**0.5) * sigma(V[i][:55], I[i][:55], V_err[i][:55], I_err[i][:55])[1]**2 / sigma(V[i][:55], I[i][:55], V_err[i][:55], I_err[i][:55])[0]**0.5 for i in range(len(V))]
plt.errorbar([1, 5, 10, 15, 20, 25], sigmas, yerr=error_sigmas, fmt = 'ok', capsize = 5)
plt.xlabel('Integration time', fontsize = 20)
plt.ylabel('Dispersion', fontsize = 20)
plt.grid(True)

#%%
import numpy as np
import Funciones as f
import matplotlib.pyplot as plt

data = np.loadtxt('C:/Users/LINE/Desktop/k2612B/results led fino/0.001/iv/1 (iv).txt', skiprows= 1)
I_led = data[:, 2]
I_sipm = data[:, 0]

I_err_sipm = f.error_I(I_sipm)
plt.errorbar(I_led, I_sipm, yerr=I_err_sipm, fmt='ok', capsize = 5)
plt.ylabel('Corriente SiPM  (A)')