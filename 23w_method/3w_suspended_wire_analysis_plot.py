# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:30:51 2019

@author: CRYOGENIC
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import sympy as sp

#fnames = ['results/GaGdN-300K-190809_001.dat',
#          'results/GaGdN-300K-190809_002.dat']
#fname = '200203//200203_P_4_power_dep_f3p4_test2_2020-02-03 15-15-13.142605.txt'
#fname = '200203//200203_P_4_power_dep_f3p4_test1_2020-02-03 14-48-22.718494.txt'
fname = '200309//200309_glass_R78_3w_measurement_1.txt'
graph_data = pd.read_csv(fname, sep = ' ', header = 0)
alpha = (0.002015 + 0.002005 + 0.001989 + 0.001988) / 4
Re0 = 39.75#38.86#40.2#39.75
V1w = 67.95e-3#66.86e-3#69.21e-3#67.95e-3
I1w = V1w / Re0
graph_data['X3_pure'] = graph_data['X3'] - graph_data['X3_ref'].mean()
T_avg = graph_data['X3_pure'] / (-1/2 * alpha * V1w)
L = 1.8e-3 #---- estimated --- #length between V1w contacts
P = V1w**2 / Re0 / L#power / unit length
C = 2.11e6
b = 10e-6
r = 0.5772 #Euler constant

x = np.log(graph_data.Lockin1f * 2 * np.pi)
y = T_avg
slope, const = np.polyfit(x,y,1)
detk = (-1/2 * P / (np.pi * slope))**2
#detk = 1
fig2, ax = plt.subplots(1,1)
ax.scatter(x,y)
ax.plot(x, x*slope + const, 'r')
ax.set_xlabel('ln(w)')
ax.set_ylabel('T(K)')
#ax.set_ylim([-1e-6, graph_data.X3.max() + 5e-6])
ax.text(5,0.31, 'slope = '+ r"$-\frac{P}{2\pi\sqrt{k_{zz}k_{xx} - k_{xz}^2}} = $" 
        + str(np.around(slope,decimals = 6)),fontsize = 14)
#plt.savefig(fname[:len(fname) - 4] + '_detk', dpi = 300)

def T_low_freq_limit(f, detk, p0):
    mag = P / (np.sqrt(detk))
    #p0 = kxx / detk
    T = mag/(np.pi) * (
            -1/2*np.log(b**2*2 * 2 * np.pi * f *C * p0) + 3/2 - r - 1j * np.pi / 4)
#    kxx = np.exp((T_avg[0] / (P/(np.pi*np.sqrt(detk))) - 3/2 + r) * (-2)) / (b**2*2*w1*C/detk)
#    T = P/(np.pi*np.sqrt(detk)) * (-1/2*np.log(0.666809706959511*kxx) + 3/2 - r)
    
    return np.real(T)

popt, pcov = curve_fit(T_low_freq_limit, graph_data['Lockin1f'], 
                       graph_data['X3_pure']/ (-1/2 * alpha * Re0 * I1w), p0 = [1,1])

mag = popt[0]
p0 = popt[1]



#w1 = graph_data['Lockin1f'][0] * 2 * np.pi
#T1 = T_avg[0]
#kxx = sp.symbols('kxx')
##eq = sp.Eq(P/(np.pi*np.sqrt(detk)) * (-1/2*sp.log(b**2*2*w1*C*kxx/detk) + 3/2 - r) - T1)
#eq = sp.Eq(0.0103 * (-1/2*sp.log(0.316 * kxx) + 0.9228) - T1)
#x = sp.solve(eq, kxx)


fig, axs = plt.subplots(1,2, figsize=(8,4)) 
axs[0].scatter(graph_data.Lockin1f, graph_data.X3, label = 'X3')
axs[0].scatter(graph_data.Lockin2f, graph_data.Y3, label = 'Y3')
x = graph_data.Lockin1f
y = T_low_freq_limit(graph_data.Lockin1f,mag,p0)
axs[0].plot(x, y, label = 'X3_fit')
#axs[0].plot(graph_data.Lockin2f, graph_data.X3_ref, label = '')
axs[0].set_xlabel('f(Hz)')
axs[0].set_ylabel('Real_V3w(V)')
axs[0].set_xscale('log')
axs[0].legend(loc = 'upper right')
axs[0].set_ylim([-1e-6, graph_data.X3.max() + 5e-6])

axs[1].scatter(graph_data.Lockin1f, graph_data.X3_ref, label = 'X3_ref')
axs[1].scatter(graph_data.Lockin2f, graph_data.Y3_ref, label = 'Y3_ref')
#axs[1].plot(graph_data.Lockin1f, graph_data.Y3, label = '')
#axs[1].plot(graph_data.Lockin2f, graph_data.Y3_ref, label = '')
axs[1].set_xlabel('f(Hz)')
axs[1].set_ylabel('Imag_V3w(V)')
axs[1].set_xscale('log')
axs[1].legend(loc = 'upper right')
axs[1].set_ylim([-10e-6, graph_data.X3_ref.max() + 10e-6])
#fig.suptitle('R43 3w measurement', fontsize = 16, x= 0.5, y = 1) 

plt.tight_layout()
#plt.savefig(fname[:len(fname) - 4],dpi = 300)
