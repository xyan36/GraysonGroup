# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:30:51 2019

@author: CRYOGENIC
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

#fnames = ['results/GaGdN-300K-190809_001.dat',
#          'results/GaGdN-300K-190809_002.dat']
#fname = '200203//200203_P_4_power_dep_f3p4_test2_2020-02-03 15-15-13.142605.txt'
#fname = '200203//200203_P_4_power_dep_f3p4_test1_2020-02-03 14-48-22.718494.txt'
fname = '200205//200205_P_4_3w_test1_2020-02-05 11-58-14.423207.txt'

graph_data = pd.read_csv(fname, sep = ' ', header = 0)

fig, axs = plt.subplots(2,1, figsize=(8,6))  
axs[0].scatter(graph_data.Lockin1f, graph_data.X3, label = 'X3')
axs[0].scatter(graph_data.Lockin2f, graph_data.X3_ref, label = 'X3_ref')
axs[0].plot(graph_data.Lockin1f, graph_data.X3, label = '')
axs[0].plot(graph_data.Lockin2f, graph_data.X3_ref, label = '')
axs[0].set_xlabel('f(Hz)')
axs[0].set_ylabel('Real_V3w(V)')
axs[0].set_xscale('log')
axs[0].legend(loc = 'upper right')
axs[0].set_ylim([graph_data.X3.min() - 0.0001, graph_data.X3.max() + 0.0002])

axs[1].scatter(graph_data.Lockin1f, graph_data.Y3, label = 'Y3')
axs[1].scatter(graph_data.Lockin2f, graph_data.Y3_ref, label = 'Y3_ref')
axs[1].plot(graph_data.Lockin1f, graph_data.Y3, label = '')
axs[1].plot(graph_data.Lockin2f, graph_data.Y3_ref, label = '')
axs[1].set_xlabel('f(Hz)')
axs[1].set_ylabel('Imag_V3w(V)')
axs[1].set_xscale('log')
axs[1].legend(loc = 'upper right')
axs[1].set_ylim([graph_data.Y3.min() - 0.0001, graph_data.Y3.max() + 0.0001])

plt.tight_layout()
#plt.savefig('200205//200205_p4_3w_test1_plot_X3_Y3',dpi = 300)
