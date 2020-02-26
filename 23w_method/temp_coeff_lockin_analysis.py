# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 10:57:57 2019

@author: xueti
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

#fhand =open("190321_temp_coeff_goldwire_test3.txt",'r')
#newf = open("190321_temp_coeff_goldwire_test3_rstrip.txt",'w')
#
#for line in fhand:
#    newline = line.rstrip()
#    newf.write(newline + '\n')
#newf.close()
df = pd.read_csv("200224//200224_23w_glass_R78_temp_coeff_5.txt", sep = ' ' ,
                 header = 0, names = ['Date_Time', 'RTD', 'Vsamp'])
df['Date_Time'] = pd.to_datetime(df['Date_Time'])
#datetime objects can be used as dictionary keys, so locate with internal index 'iloc'
axtime = df['Date_Time']-df['Date_Time'].iloc[0]
#specify type: use astype()
df['Time'] = axtime.dt.total_seconds()
df.set_index('Time',inplace = True)

#convert rtd temp to degree C
df['T'] = 9.91684E-6*df['RTD']**2+0.23605*df['RTD']-245.96823
#df['Tr'] = 9.91684E-6*df['RTDr']**2+0.23605*df['RTDr']-245.96823
#df['Tavg'] = (df['Tl'] + df['Tr']) / 2

##plot resistance vs. average T
#fig = plt.figure(1,figsize = (6,4))
#ax1 = plt.subplot(1,1,1)
#ax1.plot(df['Tavg'], df['Rsamp'])
#ax1.set_ylim([0,0.5])
#ax1.set_ylabel('R(Ohms)')
#ax1.set_xlabel('T(degree C)')

#plt.savefig('190321_gold_temp_coeff_plot_test3',dpi = 300)

#fit the coefficient : heating up
# R / Rref = 1 + alpha * (T - Tref)
Re0 = 39.75
I = df['Vsamp'].iloc[0] / Re0
df['Rsamp'] = df['Vsamp'] / I
Rref = df['Rsamp'].iloc[0]
df['dTavg'] = df['T'] - df['T'].iloc[0]

x = df['dTavg'][0:df['dTavg'].idxmax()] #average (T- Tref)
y = df['Rsamp'][0:df['dTavg'].idxmax()] / Rref   # R/Rref
m,b = np.polyfit(x,y,1)

fig = plt.figure(2,figsize = (6,6))
ax1 = plt.subplot(2,1,1)
ax1.plot(x,y,'bo',x,m*x+b,'r')
ax1.text(2,1.002,'y = '+ 
         str(np.around(m,decimals = 6))+ 
         'x + ' + str(np.around(b,decimals = 6)))
ax1.set_xlabel('dT (degree C)')
ax1.set_ylabel('R/R0(Ohms)')

#fit the coefficient : cooling down
# R / Rref = 1 + alpha * (T - Tref)
x = df['dTavg'][df['dTavg'].idxmax():] #average (T- Tref)
y = df['Rsamp'][df['dTavg'].idxmax():] / Rref   # R/Rref
m,b = np.polyfit(x,y,1)

ax1 = plt.subplot(2,1,2)
ax1.plot(x,y,'bo',x,m*x+b,'r')
ax1.text(2,1.002,'y = '+ 
         str(np.around(m,decimals = 6))+ 
         'x + ' + str(np.around(b,decimals = 6)))
ax1.set_xlabel('dT (degree C)')
ax1.set_ylabel('R/R0(Ohms)')

plt.savefig('200224_glass_1_temp_coeff_5_plot',dpi = 300)
