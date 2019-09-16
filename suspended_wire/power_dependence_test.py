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
TESTNAME = "190411_3w_sw_gold_wire" #record the frequency
rm = visa.ResourceManager();
print(rm.list_resources())
#fg = rm.open_resource("GPIB::9::INSTR")
lockin1 = rm.open_resource("GPIB::10::INSTR") #sample & SINE_OUT source
lockin2 = rm.open_resource("GPIB::8::INSTR") #reference resistor

### output file initialize ###
FILENAME = TESTNAME + '_' + str(datetime.now()).replace(':','-') + ".txt"
output = open(FILENAME,'w')
t0 = time.clock()
ti = datetime.now()
header = "Time V_input X1 Y1 X1_ref Y1_ref X3 Y3 Date_time\n"
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
    X1 = float(lockin1.query("OUTP?1"))
    Y1 = float(lockin1.query("OUTP?2"))
    X2 = float(lockin2.query("OUTP?1"))
    Y2 = float(lockin2.query("OUTP?2"))
    time.sleep(initWaitTime) #initial wait time
#    #check reading to be stable
    while (np.abs(X1 - float(lockin1.query('OUTP?1')))> sens
        or np.abs(X2 - float(lockin2.query('OUTP?1')))> sens):
        X1 = float(lockin1.query("OUTP?1"))
        Y1 = float(lockin1.query("OUTP?2"))
        X2 = float(lockin2.query("OUTP?1"))
        Y2 = float(lockin2.query("OUTP?2"))
        time.sleep(5) #additional wait time
    t = float(time.clock()-t0)
    line = str(t) + " "  \
            + str(X1) + " " + str(Y1) + " "  \
            + str(X2) + " " + str(Y2) + " " + str(datetime.now())
    print(line)
    output.write(line + '\n')

### voltage swap ###
def VoltageSweep(voltages,sens1, TC1, SENS1, sens3, TC3, SENS3, initWaitTime):
    for v in voltages:
        lockin1.write("SLVL %d" %v)
        print(str(v) + ': ')
        output.write(str(v) + " ")
        time.sleep(5) #waiting for voltage stable
        lockinInit_1w()
        lockin_set_pms(TC1,SENS1)
        measurement(sens1,initWaitTime)
        lockinInit_3w()
        lockin_set_pms(TC3,SENS3)
        measurement(sens3,initWaitTime)

freq = 17 #Hz
lockin1.write('FREQ %d' %freq)
voltages = np.array([0.004,0.1,0.15,0.2,0.25,0.3,0.35,0.4])
sens1 = #allowed error
timeCon1 = #time const for 1w measurement
sensitivity1 = #sensitivity for 1w measurement
sens3 = #allowed error
timeCon3 = #time const for 3w measurement
sensitivity3 = #sensitivity for 3w measurement
initWaitTime = 60 #s
VoltageSweep(voltages, sens1, timeCon1, sensitivity1, sens3, timeCon3, sensitivity3, initWaitTime)

output.close()# may record unfinished data
tf = datetime.now()
print ("Program done! total time is: "+ str(tf-ti))
