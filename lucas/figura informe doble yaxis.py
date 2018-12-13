import numpy as np
import matplotlib.pyplot as plt

# 868 sin led
data_sinled = np.loadtxt("C:/Users/lucas/Documents/GitHub/Labo-7/Mediciones/Vbr/Para informe/Vbr/Estacionario 2/iv/9 (iv).txt")

# 870 con led
data_conled = np.loadtxt("C:/Users/lucas/Documents/GitHub/Labo-7/Mediciones/Vbr/Mediciones LED prendido/Estacionario 2/iv/4 (iv).txt")

fig=plt.figure()
ax=fig.add_subplot(111, label="1")
ax2=fig.add_subplot(111, label="2", frame_on=False)

ax.plot(data_conled[:, 0], data_conled[:, 1], color="tab:red")
ax.set_xlabel("Voltaje [V]", color="tab:red", fontsize=18)
ax.set_ylabel("Corriente [A]", color="tab:red", fontsize=18)
ax.tick_params(axis='x', colors="tab:red")
ax.tick_params(axis='y', colors="tab:red")
plt.yscale('log')
plt.grid(True)

ax2.scatter(data_sinled[:, 0], data_sinled[:, 1], color="tab:blue")
ax2.xaxis.tick_top()
ax2.yaxis.tick_right()
ax2.set_xlabel('Voltaje [V]', color="tab:blue", fontsize=18) 
ax2.set_ylabel('Corriente [A]', color="tab:blue", fontsize=18)       
ax2.xaxis.set_label_position('top') 
ax2.yaxis.set_label_position('right') 
ax2.tick_params(axis='x', colors="tab:blue")
ax2.tick_params(axis='y', colors="tab:blue")
ax2.set_ylim(5E-9, 3E-7)
plt.yscale('log')
plt.grid(True)

plt.rc('xtick',labelsize=12)
plt.rc('ytick',labelsize=12)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

#%%

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab

path = 'C:/Users/lucas/Documents/GitHub/Labo-7/Mediciones/Rq/Estacionario 4/res/'


T = []
for i in range(1, 33):
    R_temp = np.loadtxt(path + "%s (res).txt" % i, skiprows=1)[:, 1]
    for j in range(len(R_temp)):
        T.append((R_temp[j] - 1000)/3.815)
        
(mu, sigma) = norm.fit(T)
        
n, bins, patches = plt.hist(T, bins=50)
plt.ylabel("Entradas", fontsize=20)
plt.xlabel("Temperatura [ºC]", fontsize=20)
plt.xlim(-32.06, -32)

#♠y = mlab.normpdf( bins, mu, sigma)
#l = plt.plot(bins, y, 'r--', linewidth=3)
        
        
        
        
        
        
