#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 14:45:24 2018

@author: labosat
"""


import numpy as np
import matplotlib.pyplot as plt


def Error(weights):
    temp = [i/np.sqrt(len(weights)) for i in weights]
    return np.mean(temp)

folders = 12
path = '/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones_temporarias/'

T = []
Vbr = []
T_err = []
Vbr_err = []
for i in range(1, folders + 1):
    data = np.loadtxt(path + "%s.txt" % i)
    T_temp = data[:, 0]
    Vbr_temp = data[:, 1]
    T_err_temp = data[:, 2]
    Vbr_err_temp = data[:, 3]
    
    T.append(np.mean(T_temp))
    Vbr.append(np.mean(Vbr_temp))
    T_err.append(Error(T_err_temp))
    Vbr_err.append(Error(Vbr_err_temp))
    
plt.errorbar(T, Vbr, xerr=T_err, yerr=Vbr_err, fmt='.', capsize=3)
plt.grid(True)

Vbr_err2 = [1/x for x in Vbr_err]

plt.plot(T, np.polyval(np.polyfit(T, Vbr, w=Vbr_err2, deg=1), T))
np.polyfit(T, Vbr, w=Vbr_err2, deg=1, full=True)

np.savetxt("/home/labosat/Desktop/Finazzi-Ferreira/Labo-7/Mediciones/Graficos y txt/txts/vbr_final.txt", np.c_[T, Vbr, T_err, Vbr_err])
