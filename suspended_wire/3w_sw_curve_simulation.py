# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 12:23:39 2020

@author: xueti
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

## Temperature coefficient of resistance alpha:
alpha = 0.005 #/K
## Sample resistance of room temperature Re0:
Re0 = 2.7 #ohms
## 1w voltage on sample:
#V1w = 
## 1w current on sample
I1w = 0.0051 #A 
#or 
#Iw = V1w / Re0
## Suspended length of sample full_l:
full_l = 0.004 #m
l = full_l / 2 #l in the formula is HALF-length of suspended wire
## Thermal conductivity k:
k = 1 #W/mK
## Cross-sectional area S:
S = 0.5e-6 #m^2
## Density of sample:
rou = 7.7e3 #kg/m^3
## Specific heat capacity of sample:
cp = 165 #J/kgK
## Frequency range to be plotted:
start = 0.0001#in Hz
stop =  1#in Hz
num_of_total_points = 1000
freqs = np.linspace(start, stop, num_of_total_points)

def V3w_real(freqs): 
    w1 = 2 * np.pi * freqs
    K = k / (rou * cp) # thermal diffusivity
    tau = 4*l**2/K
    V3wreal = - alpha * Re0**2 * I1w**3 * l / (12 * k * S)  \
    * (1 / (1 + (w1 * tau / 5)**2))
    return V3wreal
def V3w_imag(freqs):
    w1 = 2 * np.pi * freqs
    K = k / (rou * cp) # thermal diffusivity
    tau = 4*l**2/K
    V3wimag = alpha * Re0**2 * I1w**3 * l / (12 * k * S)  \
    * (w1 * tau / 5) / (1 + (w1 * tau / 5)**2)
    return V3wimag

X3 = V3w_real(freqs)
Y3 = V3w_imag(freqs)
fig, axs =  plt.subplots(1,2, figsize = (12,6))
axs[0].plot(freqs, X3, label = 'X3') 
axs[0].set_xlabel('f(Hz)')
axs[0].set_ylabel('V3w(V)')
axs[0].legend()
axs[1].plot(freqs, Y3, label = 'Y3')  
axs[1].set_xlabel('f(Hz)')
axs[1].set_ylabel('V3w(V)')
axs[1].legend()
plt.tight_layout()
#fig.savefig('name.jpg', dpi = 300)

result = pd.DataFrame({'f(Hz)' : freqs, 'X3(V)' : X3, 'Y3(V)' : Y3})
result.to_csv('3w_simulation_data.csv', index = False)




