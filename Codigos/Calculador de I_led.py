import numpy as np
import matplotlib.pyplot as plt

N = 40  #numero de puntos por curva
x_min = 0.001 #corriente mas chica luego del 0
x_max = 20  #corriente mas alta, tipicamente 20 mA
a = (1/(N-1)) * np.log10(x_max/x_min)
b = np.arange(0, N, 1)
c = [x_min * 10**(i*a) for i in b]  #corrientes que le vamos a mandar al LED



plt.plot(c, 'o')  #para ver que es lineal en escala logaritmica
plt.yscale('log')
