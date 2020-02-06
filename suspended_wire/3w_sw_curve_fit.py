# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:04:37 2019

@author: xueti
"""
### suspended wire curve fitting ###
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os
import sys

fname = '200205//200205_P_4_3w_test1_2020-02-05 11-58-14.423207.txt'
graph_data = pd.read_csv(fname, sep = ' ')

a = 0.0026 #temperature coefficient
Re0 = 3.5#resistance at RT
V1w_sp = 80e-3
I1w = V1w_sp/Re0#V1w / Re0   
l = 5e-3/2#half length of wire
D = 0.025e-3; #m diameter
S = np.pi*(D/2)**2  #crosssectional area
rou = 0.01e-3/S #kg/m^3 gold
#rou = 21.45*10**3 #kg/m^3
#tau = 4*l**2/K * rou * c
#Rth = 2*l / K / S
#k = 70.9  #w/mK thermal conductivity
#c = 131.2 #J/kgK

def V3w_real(w1, k, c):   
    tau = 4*l**2/k * rou * c
    V3wreal = - a*Re0**2*I1w**3*l/(12*k*S)*(1/(1+(w1*tau/5)**2))
    return V3wreal

def V3w_imag(w1, k, c):
    tau = 4*l**2/k * rou * c
    V3wimag = a*Re0**2*I1w**3*l/(12*k*S)*(w1*tau/5)/(1+(w1*tau/5)**2)
    return V3wimag

def writeCSV(dataframe, fname):
    if os.path.isfile(fname):
        check = input(fname + ' File exist. Overwrite? y/n: ')
        if check == 'y':
            dataframe.to_csv(fname, index = False)
            return
        else:
            print('Oops. Don\'t forget to change file name:D')
            return
    else:
        dataframe.to_csv(fname, index = False)
    return

w1 = graph_data['Lockin1f']*2*np.pi #use w = 2pi*f to fit
popt_X3, pcov_X3 = curve_fit(V3w_real, w1, graph_data['X3'], p0 = [10,10])
popt_Y3, pcov_Y3 = curve_fit(V3w_imag, w1, graph_data['Y3'], p0 = [10, 10])

#df2 = pd.DataFrame({'freq': w1/(2*np.pi), 'w1':w1, 'X1_fit': V3w_real(w1,*popt), 'X1_exp': V3w_real(w1, 314, 130),
#                    'Y1_fit': V3w_imag(w1,*popt2), 'Y1_exp': V3w_imag(w1, 314, 130)})

fig, axs = plt.subplots(2,1,figsize = (8,10))
axs[0].scatter(graph_data.Lockin1f, graph_data.X3, label = 'X3')
axs[0].plot(graph_data.Lockin1f, V3w_real(w1,*popt_X3), label = 'X3_fit')
axs[0].set_xlabel('f(Hz)')
axs[0].set_ylabel('Real_V3w(V)')
axs[0].set_xscale('log')
axs[0].set_xlim(0.01,100)
axs[0].legend(loc = 'upper right')
axs[0].set_ylim(graph_data.X3.min() - 0.0001, graph_data.X3.max() + 0.0002)

axs[1].scatter(graph_data.Lockin1f, graph_data.Y3, label = 'Y3')
axs[1].plot(graph_data.Lockin1f, V3w_imag(w1, *popt_Y3), label = 'Y3_fit')
axs[1].set_xlabel('f(Hz)')
axs[1].set_ylabel('Imag_V3w(V)')
axs[1].set_xscale('log')
axs[1].set_xlim(0.01,100)
axs[1].legend(loc = 'upper right')
axs[1].set_ylim(graph_data.Y3.min() - 0.0001, graph_data.Y3.max() + 0.0001)

#plt.subplots_adjust(hspace = 0.2,wspace = 0.2)
plt.tight_layout()
#plt.savefig('190923_3w_sw_Sintered_P_1_V0074',dpi = 300)
#writeCSV(df,'190526_1st_goldwire_Si_4V.csv')
#writeCSV(df2, '190526_1st_goldwire_Si_4V_edited.csv')

