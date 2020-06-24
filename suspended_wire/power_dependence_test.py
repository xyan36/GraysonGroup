# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:05:51 2019

@author: Administrator
"""

from datetime import datetime
import time
import visa
import numpy as np
import os

########### function defitions ################################################
### lock in 1w initialize ###
def lockinInit_1w():
    #set lockin1 to internal (1), lockin2 to external(0)
    #lockin1.write("FMOD 0")
    #lockin2.write("FMOD 0")
    #set lockins to measure the 1w voltage
    lockin1.write("HARM 1")
    lockin2.write("HARM 1")
#    #make phases zero
#    lockin1.write("PHAS 0")
#    lockin2.write("PHAS 0")
#    #set input configuration
#    lockin1.write("ISRC 1")
#    lockin2.write("ISRC 1")
#    #ground type
#    lockin1.write("IGND 1")
#    lockin2.write("IGND 1")
#    #input coupling
#    lockin1.write("ICPL 1")
#    lockin2.write("ICPL 1")
#    #reserve mode
#    lockin1.write("RMOD 1")
#    lockin2.write("RMOD 1")

### lock in 3w initialize ###
def lockinInit_3w():
    #set lockins to measure the 3w voltage
    lockin1.write("HARM 3")
    lockin2.write("HARM 3")
    #reserve mode
    lockin1.write("RMOD 1")
    lockin2.write("RMOD 1")

def lockin_set_pms(timeCon,sensitivity):
    #time constant
    lockin1.write("OFLT %d" %timeCon)
    lockin2.write("OFLT %d" %timeCon)
    #sensitivity
    lockin1.write("SENS %d" %sensitivity)
    lockin2.write("SENS %d" %sensitivity)

### measurements ###
def measurement(sens,initWaitTime): #sens= allowed error in reading
    X = float(lockin1.query("OUTP?1"))
    Y = float(lockin1.query("OUTP?2"))
    X_ref = float(lockin2.query("OUTP?1"))
    Y_ref = float(lockin2.query("OUTP?2"))
    time.sleep(initWaitTime) #initial wait time
#    #check reading to be stable
    while (np.abs(X - float(lockin1.query('OUTP?1')))> sens
        or np.abs(X_ref - float(lockin2.query('OUTP?1')))> sens):
        X = float(lockin1.query("OUTP?1"))
        Y = float(lockin1.query("OUTP?2"))
        X_ref = float(lockin2.query("OUTP?1"))
        Y_ref = float(lockin2.query("OUTP?2"))
        time.sleep(5) #additional wait time
    line = str(X) + " " + str(Y) + " "  \
            + str(X_ref) + " " + str(Y_ref) + " "
    return line

### voltage swap ###
def VoltageSweep(voltages,sens1, TC1, SENS1, initWaitTime1, sens3, TC3, SENS3, initWaitTime3):
    for v in voltages:
        lockin1.write("SLVL %f" %v)
        line = str(v) + " "
        time.sleep(5) #waiting for voltage stable
        lockinInit_1w()
        lockin_set_pms(TC1,SENS1)
        str(datetime.now())
        line += measurement(sens1,initWaitTime1)
        lockinInit_3w()
        lockin_set_pms(TC3,SENS3)
        line += measurement(sens3,initWaitTime3).rstrip()
        t = float(time.time()-t0)
        print(str(datetime.now()) + " " + str(t) + " " + line)
        with open(FILENAME,'a') as output:
            output.write(str(datetime.now()) + " " + str(t) + " " + line +"\n")
 ##############################################################################

### crate a folder with today's date and create a new file name ###
date = '200624'
try:
    os.mkdir(date)
except FileExistsError:
    pass
FILENAME = f"{date}//{date}_Bi2Te30617_power_dep_f3p4.txt"

rm = visa.ResourceManager();
print(rm.list_resources())
lockin1 = rm.open_resource("GPIB2::9::INSTR") #sample & SINE_OUT source
lockin2 = rm.open_resource("GPIB2::18::INSTR") #reference resistor
t0 = time.time()
ti = datetime.now()
header = "Date time Time V_input X1 Y1 X1_ref Y1_ref X3 Y3 X3_ref Y3_ref\n"
with open(FILENAME,'w') as output:
    output.write(header)

### Set the parameters ###
freq = 3.4 #Hz
voltages = np.array([0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3])
sens1 = 1e-3#allowed error for 1w
timeCon1 = 13#time const for 1w measurement
sensitivity1 = 24#sensitivity for 1w measurement
initWaitTime1 = 150 #s

sens3 = 1e-6#allowed error for 3w
timeCon3 = 13#time const for 3w measurement
sensitivity3 = 14#sensitivity for 3w measurement
initWaitTime3 = 300 #s

lockin1.write('FREQ %f' %freq)
VoltageSweep(voltages, sens1, timeCon1, sensitivity1, initWaitTime1,
            sens3, timeCon3, sensitivity3, initWaitTime3)

lockin1.write("SLVL %f" %0.004)
lockinInit_1w()
output.close()# may record unfinished data
tf = datetime.now()
print ("Program done! total time is: "+ str(tf-ti))
