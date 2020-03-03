# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:27:47 2020

@author: xueti
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#fname = '200227//200227_glass_R78_R1516_2w_measurement_3.txt'
fname = "200302//200302_glass_R65_R1817_2w_measurement_1.txt"
fig, axs = plt.subplots(1,2, figsize=(8,4))
graph_data = pd.read_csv(fname, sep = ' ', header = 0,
                         names = ['Date_time','Time','TC','SENS','Lockin1f','Lockin2f','X2','Y2','X1','Y1'])
  
axs[0].scatter(graph_data.Lockin1f, graph_data.X2, label = 'X2')
axs[0].scatter(graph_data.Lockin2f, graph_data.Y2, label = 'Y2')
#axs[0].plot(graph_data.Lockin1f, graph_data.X2)
#axs[0].plot(graph_data.Lockin2f, graph_data.Y2)
axs[0].set_xlabel('f(Hz)')
axs[0].set_ylabel('Real_V3w(V)')
axs[0].set_xscale('log')
axs[0].set_ylim([-100e-6, 300e-6])
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
plt.savefig("200302//200302_glass_R65_R1817_2w_measurement_1_plot", dpi = 300)