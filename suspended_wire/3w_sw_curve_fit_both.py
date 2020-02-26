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

fname = '200206//200206_P_4_3w_test12_combined.txt'
graph_data = pd.read_csv(fname, sep = ' ')

a = 5e-3#temperature coefficient --need remeasure for better accuracy
Re0 = 2.7#resistance at RT
#Rref =
V1w_sp = 67.71e-3
I1w = V1w_sp/Re0#V1w / Re0   
l = 4e-3/2#half length of wire(= half gap width)
width = 2e-3; #mm line width --
thickness = 17e-6 #mm line thickness --
S = width * thickness  #crosssectional area
rou =  7.74e3#kg/m^3 density
#correction_factor = 1 - 1.5 / (50 + 2.7 + 3.5) # 1 - R_all_3w_parts / R_total


#rou = 21.45*10**3 #kg/m^3
#tau = 4*l**2/K * rou * c
#Rth = 2*l / K / S
#k = 70.9  #w/mK thermal conductivity
#c = 131.2 #J/kgKS

def V3w_real(w1, k, c, correction_factor = 1):   
    tau = 4*l**2/k * rou * c
    V3wreal = - a*Re0**2*I1w**3*l/(12*k*S)*(1/(1+(w1*tau/5)**2))
    return V3wreal

def V3w_imag(w1, k, c, correction_factor = 1):
    tau = 4*l**2/k * rou * c
    V3wimag = a*Re0**2*I1w**3*l/(12*k*S)*(w1*tau/5)/(1+(w1*tau/5)**2)
    return V3wimag

def V3w_fit_both(w1, k, c, correction_factor = 1):
    
    fit_real = V3w_real(w1[:len(graph_data.X3)], k, c)
    fit_imag = V3w_imag(w1[len(graph_data.Y3):], k, c)
    
    return np.append(fit_real, fit_imag)
    

def writeCSV(dataframe, fname):
    if os.path.isfile(fname):
        check = input('Trying to write: ' + str(dataframe.columns) + ' to ' + fname + '. File exist. Overwrite or append or cancel? o/a/c: ')
        if check == 'o':
            dataframe.to_csv(fname, index = True)
            return
        elif check== 'a':
            with open(fname, 'a') as output:
                dataframe.to_csv(output, header = True)
        else:
            print('Oops. Don\'t forget to change file name:D')
            return
    else:
        dataframe.to_csv(fname, index = True)
    return

w1 = np.arange(0.01,100,0.01) * 2* np.pi#use w = 2pi*f to fit
#popt_X3, pcov_X3 = curve_fit(V3w_real, graph_data.Lockin1f * 2* np.pi, graph_data['X3'], p0 = [10,10])
#popt_Y3, pcov_Y3 = curve_fit(V3w_imag, graph_data.Lockin1f * 2* np.pi, graph_data['Y3'], p0 = [10, 10])

combo_Xdata = np.append(graph_data.Lockin1f * 2 * np.pi, graph_data.Lockin1f * 2 * np.pi)
combo_Ydata = np.append(graph_data.X3, graph_data.Y3)
popt, pcov = curve_fit(V3w_fit_both, combo_Xdata, combo_Ydata, p0 = [10, 10])

result = pd.DataFrame({'fit values': popt}, 
                      index = ['Thermal conductivity k', 'Heat capacity c'],
                      )
parameters = pd.DataFrame({'Temp coeff a': a, 'Re0': Re0, 'V1w_sp': V1w_sp,
                       'I1w': I1w, 'Suspended length 2l': 2*l, 
                       'Width': width, 'Thickness': thickness,
                       'S': S, 'Density': rou}, index = ['Parameter values:'],
                        )
parameters = parameters[['Temp coeff a', 'Re0', 'V1w_sp', 'I1w', 
                         'Suspended length 2l', 'Width', 'Thickness',
                         'S', 'Density']] #reorder columns
fig, axs = plt.subplots(2,1,figsize = (8,10))
axs[0].scatter(graph_data.Lockin1f, graph_data.X3, label = 'X3')
axs[0].plot(w1 / 2 / np.pi, V3w_real(w1,*popt), label = 'X3_fit')
axs[0].set_xlabel('f(Hz)')
axs[0].set_ylabel('Real_V3w(V)')
axs[0].set_xscale('log')
axs[0].set_xlim(0.01,100)
axs[0].legend(loc = 'upper right')
axs[0].set_ylim(graph_data.X3.min() - 0.0001, graph_data.X3.max() + 0.0002)

axs[1].scatter(graph_data.Lockin1f, graph_data.Y3, label = 'Y3')
axs[1].plot(w1 / 2 / np.pi, V3w_imag(w1, *popt), label = 'Y3_fit')
axs[1].set_xlabel('f(Hz)')
axs[1].set_ylabel('Imag_V3w(V)')
axs[1].set_xscale('log')
axs[1].set_xlim(0.01,100)
axs[1].legend(loc = 'upper right')
axs[1].set_ylim(graph_data.Y3.min() - 0.0001, graph_data.Y3.max() + 0.0001)

#plt.subplots_adjust(hspace = 0.2,wspace = 0.2)
plt.tight_layout()
plt.savefig('200206//200206_P_4_3w_fit_2_both',dpi = 300)
output = '200206//200206_P_4_3w_fit_result_2.csv'
writeCSV(parameters, output)
writeCSV(result, output)

