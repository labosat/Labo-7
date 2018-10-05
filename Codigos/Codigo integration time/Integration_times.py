import numpy as np
import matplotlib.pyplot as plt
import Funciones as f
from Funciones import Linear
import sys
sys.path.append('./Labo-7/')
from scipy.odr import Model, RealData, ODR

path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Integration Time'

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
    return f.dispersion(recta)
    
sigmas = []
g, ([ax1, ax2, ax3], [ax4, ax5, ax6]) = plt.subplots(2, 3)
g.tight_layout()
ax1.plot(V[0][:55], I[0][:55], '.')
a = sigma(V[0][:55], I[0][:55], V_err[0][:55], I_err[0][:55])
sigmas.append(a)
#ax1.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax1.set_title('Integration time = 1')
ax1.set_xlabel('V')
ax1.set_ylabel('I (A)')
ax2.plot(V[1][:55], I[1][:55], '.')
a = sigma(V[1][:55], I[1][:55], V_err[1][:55], I_err[1][:55])
sigmas.append(a)
#ax2.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax2.set_xlabel('V')
ax2.set_ylabel('I (A)')
ax2.set_title('Integration time = 5')
ax3.plot(V[2][:55], I[2][:55], '.')
a = sigma(V[2][:55], I[2][:55], V_err[2][:55], I_err[2][:55])
sigmas.append(a)
#ax3.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax3.set_xlabel('V')
ax3.set_ylabel('I (A)')
ax3.set_title('Integration time = 10')
ax4.plot(V[3][:55], I[3][:55], '.')
a = sigma(V[3][:55], I[3][:55], V_err[3][:55], I_err[3][:55])
sigmas.append(a)
#ax4.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax4.set_xlabel('V')
ax4.set_ylabel('I (A)')
ax4.set_title('Integration time = 15')
ax5.plot(V[4][:55], I[4][:55], '.')
a = sigma(V[4][:55], I[4][:55], V_err[4][:55], I_err[4][:55])
sigmas.append(a)
#ax5.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax5.set_xlabel('V')
ax5.set_ylabel('I (A)')
ax5.set_title('Integration time = 20')
ax6.plot(V[5][:55], I[5][:55], '.')
a = sigma(V[5][:55], I[5][:55], V_err[5][:55], I_err[5][:55])
sigmas.append(a)
#ax6.text(22.5, 0.000000005, r'$\sigma$ = %s' % a)
ax6.set_xlabel('V')
ax6.set_ylabel('I (A)')
ax6.set_title('Integration time = 25')



plt.figure(2)
plt.plot([1, 5, 10, 15, 20, 25], sigmas, 'o')
plt.xlabel('Integration time')
plt.ylabel('Dispersion')