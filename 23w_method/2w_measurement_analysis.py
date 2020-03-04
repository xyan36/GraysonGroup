# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:27:47 2020

@author: xueti
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#fname = '200227//200227_glass_R78_R1516_2w_measurement_3.txt'
fname = "200228//200228_glass_R78_R1516_2w_measurement_5.txt"
fig, axs = plt.subplots(1,2, figsize=(8,4))
graph_data = pd.read_csv(fname, sep = ' ', header = 0,
                         names = ['Date_time','Time','TC','SENS','Lockin1f','Lockin2f','X2','Y2','X1','Y1'])

X = graph_data.X2
Y = graph_data.Y2
R = np.sqrt(X**2 + Y**2)
theta = np.arctan(Y/ X)
theta2 = theta.copy()
pdiff = theta.iloc[1] - theta.iloc[0]
i_turn = 1
for i_turn in range(2,len(theta),1):
    cdiff = theta.iloc[i_turn] - theta.iloc[i_turn - 1]
    if pdiff * cdiff < 0:
        break
    pdiff = cdiff
if i_turn > 1:
    theta2.iloc[i_turn:] = np.pi * 2 * np.sign(pdiff) + theta.iloc[i_turn:]

#result = pd.DataFrame({'X2': X, 'Y2' : Y, 'R' : R, 'theta' : theta, 
#                       'modified X2' : R * np.cos(theta - 90), 
#                       'modified Y2' : R * np.sin(theta - 90)})
##fname2 = '200303//200303_glass_R43_R2019_2w_modified.csv'
#result.to_csv(fname2, index = False)
  
axs[0].scatter(graph_data.Lockin1f, R * np.cos(theta2 - 90), label = 'X2')
axs[0].scatter(graph_data.Lockin2f, R * np.sin(theta2 - 90), label = 'Y2')
#axs[0].plot(graph_data.Lockin1f, graph_data.X2)
#axs[0].plot(graph_data.Lockin2f, graph_data.Y2)
axs[0].set_xlabel('f(Hz)')
axs[0].set_ylabel('Real_V3w(V)')
axs[0].set_xscale('log')
axs[0].set_ylim([-400e-6, 200e-6])
#    axs[0].set_xscale('log')
axs[0].legend(loc = 'upper right')

axs[1].scatter(graph_data.Lockin1f, graph_data.X1, label = 'X1')
axs[1].scatter(graph_data.Lockin2f, graph_data.Y1, label = 'Y1')
axs[1].plot(graph_data.Lockin1f, graph_data.X1)
axs[1].plot(graph_data.Lockin2f, graph_data.Y1)

axs[1].set_xlabel('f(Hz)')
axs[1].set_ylabel('Imag_V3w(V)')
#    axs[1].set_xscale('log')
axs[1].legend(loc = 'upper right')

plt.tight_layout()
#plt.savefig("200302//200302_glass_R65_R1817_2w_measurement_1_plot_n90phase", dpi = 300)