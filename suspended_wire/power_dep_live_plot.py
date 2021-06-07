# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:30:51 2019

@author: CRYOGENIC
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import pandas as pd
from IPython import get_ipython
mgc = get_ipython().magic
mgc(u'%matplotlib qt')

font = {'size'   : 7}
matplotlib.rc('font', **font)
style.use('fivethirtyeight')
colors = ['b', 'g']
interval = 1000

#fnames = ['results/GaGdN-300K-190809_001.dat',
#          'results/GaGdN-300K-190809_002.dat']
#fname = '200203//200203_P_4_power_dep_f3p4_test2_2020-02-03 15-15-13.142605.txt'
#fname = '200203//200203_P_4_power_dep_f3p4_test1_2020-02-03 14-48-22.718494.txt'
fname = '210604//210604_Bi2Te3_n7_power_dep_f3p4_1.txt'
#x_column = 'B_digital'
#y_column = 'V_real_12'
#x_columns = ['B_digital', 'B_digital']#, 'B_digital']
#y_columns = ['V_real_8', 'V_real_12']#, 'V_real_11']



#def animate(i, ax, fname, x_column, y_column):
#    graph_data = pd.read_csv(fname, skipinitialspace=True)
#    x = graph_data[x_column]
#    y = graph_data[y_column]
#    ax.clear()
#    ax.plot(x,y)
#    plt.xlabel(x_column)
#    plt.ylabel(y_column)
#    plt.tight_layout()
    
def animate_multi(i, axs, fname, color=None):
    for ax in axs:
        ax.clear()
    graph_data = pd.read_csv(fname, sep = ',', header = 0)
    Rref = 3.0#10.029
    graph_data['I1w'] = graph_data['X1_ref']/Rref
#    axs[0].plot(graph_data.Time, graph_data.X1, label = 'X1')
#    axs[0].plot(graph_data.Time, graph_data.Y1, label = 'Y1')
    axs[0].plot(graph_data.Time, graph_data.X1_ref, marker = 'o', label = 'X1_ref')
    axs[0].plot(graph_data.Time, graph_data.Y1_ref, marker = 'o', label = 'Y1_ref')
    axs[0].set_xlabel('times(s)')
    axs[0].set_ylabel('V1w(V)')
    axs[0].legend(loc = 'upper right')
    
    axs[1].plot(graph_data.Time, graph_data.X3, marker = 'o', label = 'X3')
    axs[1].plot(graph_data.Time, graph_data.Y3, marker = 'o', label = 'Y3')
#    axs[1].plot(graph_data.Time, graph_data.X3_ref, label = 'X3_ref')
#    axs[1].plot(graph_data.Time, graph_data.Y3_ref, label = 'Y3_ref')
    axs[1].set_xlabel('times(s)')
    axs[1].set_ylabel('V3w(V)')
    axs[1].legend(loc = 'upper right')
    #axs[2].legend(loc = 'lower left')

    axs[2].plot((graph_data['I1w'])**3, graph_data.X3, marker = 'o', label = 'X3')
    axs[2].plot((graph_data['I1w'])**3, graph_data.Y3, marker = 'o', label = 'Y3')
    axs[2].set_xlabel('I1w^3(A^3)')
    axs[2].set_ylabel('V3w(V)')
    axs[2].legend(loc = 'upper right')

    plt.tight_layout()
  
    '''
def animate_multi_files(i, axs, fnames, x_columns, y_columns, colors=None):
    for ax in axs.flatten():
        ax.clear()
    for fname, color in zip(fnames, colors):
        graph_data = pd.read_csv(fname, skipinitialspace=True)
        for x_column, y_column, ax in zip(x_columns, y_columns, axs[0]):
            x = graph_data[x_column]
            y = graph_data[y_column]
#            ax.clear()
            ax.plot(x,y, color=color)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
        graph_data = graph_data[graph_data['flag'] != 0]
        for x_column, y_column, ax in zip(x_columns, y_columns, axs[1]):
            x = graph_data[x_column]
            y = graph_data[y_column]
#            ax.clear()
            ax.plot(x,y,'x', color=color)
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
    plt.tight_layout()
    '''
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#ani = animation.FuncAnimation(fig, animate, fargs=[ax, fname, x_column, y_column], interval=1000)
fig, axs = plt.subplots(3,1, figsize=(8,6))
ani = animation.FuncAnimation(fig, animate_multi, fargs=[axs, fname, colors], interval=interval)
#animate_multi(1,axs,fname,colors)
plt.show()