# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:05:51 2019

@author: Administrator
"""

from datetime import datetime
import time
import visa
import numpy as np

### basic parameters ###
TESTNAME = "200203//200203_P_4_power_dep_f3p4_test3" #record the frequency
rm = visa.ResourceManager();
print(rm.list_resources())
#fg = rm.open_resource("GPIB::9::INSTR")
lockin1 = rm.open_resource("GPIB2::9::INSTR") #sample & SINE_OUT source
lockin2 = rm.open_resource("GPIB2::18::INSTR") #reference resistor

### output file initialize ###
FILENAME = TESTNAME + '_' + str(datetime.now()).replace(':','-') + ".txt"

t0 = time.time()
ti = datetime.now()
header = "Date_time Time V_input X1 Y1 X1_ref Y1_ref X3 Y3 X3_ref Y3_ref\n"
with open(FILENAME,'a') as output:
    output.write(header)

### lock in initialize ###
def lockinInit_1w():
    #set lockin1 to internal (1), lockin2 to external(0)
    #lockin1.write("FMOD 0")
    #lockin2.write("FMOD 0")
    #set lockins to measure the 1w voltage
    lockin1.write("HARM 1")
    lockin2.write("HARM 1")
    #make phases zero
    lockin1.write("PHAS 0")
    lockin2.write("PHAS 0")
    #set input configuration
    lockin1.write("ISRC 1")
    lockin2.write("ISRC 1")
    #ground type
    lockin1.write("IGND 1")
    lockin2.write("IGND 1")
    #input coupling
    lockin1.write("ICPL 1")
    lockin2.write("ICPL 1")
    #reserve mode
    lockin1.write("RMOD 1")
    lockin2.write("RMOD 1")
    #sensitivity
    #lockin1.write("SENS 22")
    #lockin2.write("SENS 22")
    #time constant
    #lockin1.write("OFLT 9")
    #lockin2.write("OFLT 9")

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


freq = 3.4 #Hz
lockin1.write('FREQ %f' %freq)
voltages = np.array([0.004,0.068, 0.338, 0.668, 0.996, 1.316, 1.632, 1.962, 2.554])
sens1 = 1e-3#allowed error
timeCon1 = 10#time const for 1w measurement
sensitivity1 = 23#sensitivity for 1w measurement
initWaitTime1 = 60 #s

sens3 = 1e-6#allowed error
timeCon3 = 11#time const for 3w measurement
sensitivity3 = 15#sensitivity for 3w measurement
initWaitTime3 = 180 #s
VoltageSweep(voltages, sens1, timeCon1, sensitivity1, initWaitTime1, sens3, timeCon3, sensitivity3, initWaitTime3)

output.close()# may record unfinished data
tf = datetime.now()
print ("Program done! total time is: "+ str(tf-ti))
