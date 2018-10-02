import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('./Labo-7/')

path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Integration Time'

I = []
V = []
for i in np.arange(0, 30, 5):
        data = np.loadtxt(path + '/Integration %s/iv/1 (iv).txt' % i, skiprows=1)
        I.append(data[:, 1])
        V.append(data[:, 0])        
        #I.append(data[:56, 1])
        #V.append(data[:56, 0])

    
f, ([ax1, ax2, ax3], [ax4, ax5, ax6]) = plt.subplots(2, 3)
f.tight_layout()
ax1.plot(V[0], I[0], '.')
#ax1.text(22, 0.0000025, 'Integration time = 0')
ax1.set_title('Integration time = 0')
ax1.set_xlabel('V')
ax1.set_ylabel('I (A)')
ax2.plot(V[1], I[1], '.')
#ax2.text(22, 0.0000025, 'Integration time = 5')
ax2.set_xlabel('V')
ax2.set_ylabel('I (A)')
ax2.set_title('Integration time = 5')
ax3.plot(V[2], I[2], '.')
#ax3.text(22, 0.0000025, 'Integration time = 10')
ax3.set_xlabel('V')
ax3.set_ylabel('I (A)')
ax3.set_title('Integration time = 10')
ax4.plot(V[3], I[3], '.')
#ax4.text(22, 0.0000025, 'Integration time = 15')
ax4.set_xlabel('V')
ax4.set_ylabel('I (A)')
ax4.set_title('Integration time = 15')
ax5.plot(V[4], I[4], '.')
#ax5.text(22, 0.0000025, 'Integration time = 20')
ax5.set_xlabel('V')
ax5.set_ylabel('I (A)')
ax5.set_title('Integration time = 20')
ax6.plot(V[5], I[5], '.')
#ax6.text(22, 0.0000025, 'Integration time = 25')
ax6.set_xlabel('V')
ax6.set_ylabel('I (A)')
ax6.set_title('Integration time = 25')