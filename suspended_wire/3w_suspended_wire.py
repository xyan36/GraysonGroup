# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:05:51 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 11:00:10 2019

@author: Administrator
"""

from datetime import datetime
import time
import visa
import numpy as np
import os
### basic parameters ###
try:
    os.mkdir('200206')
except FileExistsError:
    pass    
TESTNAME = "200206//200206_P_4_3w_test2_0p01_1"
rm = visa.ResourceManager();
print(rm.list_resources())
#fg = rm.open_resource("GPIB::11::INSTR")
lockin1 = rm.open_resource("GPIB2::9::INSTR") #sample
lockin2 = rm.open_resource("GPIB2::18::INSTR") #reference resistor
#mm1 = rm.open_resource("GPIB::2::INSTR")
#lockin1.timeout = 25000
#lockin2.timeout = 25000

### output file initialize ###
FILENAME = TESTNAME + '_' + str(datetime.now()).replace(':','-') + ".txt"
output = open(FILENAME,'w')
t0 = time.time()
ti = datetime.now()
header = "Date_time Time TC SENS Lockin1f Lockin2f X3 Y3 X3_ref Y3_ref\n"
with open(FILENAME, 'a') as output:
    output.write(header)

### lock in initialize ###
def lockinInit_1w():
    #set lockin1 to internal (1), lockin2 to external(0)
    lockin1.write("FMOD 0")
    lockin2.write("FMOD 0")
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
    #input coupling ac 0 dc 1
    lockin1.write("ICPL 1")
    lockin2.write("ICPL 1")
    #reserve mode
    lockin1.write("RMOD 1")
    lockin2.write("RMOD 1")
    #sensitivity
    lockin1.write("SENS 22")
    lockin2.write("SENS 22")
    #time constant
    lockin1.write("OFLT 9")
    lockin2.write("OFLT 9")  
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
def lockinsingle_set_pms(lockin, timeCon, sensitivity):
    #time constant
    lockin.write("OFLT %d" %timeCon)
    #sensitivity
    lockin.write("SENS %d" %sensitivity)

### measurements ###
def measurement(f1,f2,sens,initWaitTime): #sens= allowed error in reading
    X3 = float(lockin1.query("OUTP?1"))
    Y3 = float(lockin1.query("OUTP?2"))
    X3_ref = float(lockin2.query("OUTP?1"))
    Y3_ref = float(lockin2.query("OUTP?2"))
    time.sleep(initWaitTime) #initial wait time
    X33 = float(lockin1.query("OUTP?1"))
#    Y11 = float(lockin1.query("OUTP?2"))
    X33_ref = float(lockin2.query("OUTP?1"))
#    Y22 = float(lockin2.query("OUTP?2"))
    #check reading to be stable
    while (np.abs(X3 - X33)> sens
        or np.abs(X3_ref - X33_ref)> sens):
        X33 = float(lockin1.query("OUTP?1"))
#        Y11 = float(lockin1.query("OUTP?2"))
        X33_ref = float(lockin2.query("OUTP?1"))
#        Y22 = float(lockin2.query("OUTP?2"))
        time.sleep(5) #additional wait time
        X3 = float(lockin1.query("OUTP?1"))
        Y3 = float(lockin1.query("OUTP?2"))
        X3_ref = float(lockin2.query("OUTP?1"))
        Y3_ref = float(lockin2.query("OUTP?2"))     
    t = float(time.time()-t0)
    timeCon = int(lockin1.query('OFLT?'))
    SENS = int(lockin1.query('SENS?'))
    line = str(datetime.now()) + str(t) + " " \
    + str(timeCon) + " " + str(SENS) + " "  \
    + str(f1) + " " + str(f2) + " "  \
    + str(X3) + " " + str(Y3) + " "  \
    + str(X3_ref) + " " + str(Y3_ref)
    print(line)
    with open(FILENAME, 'a') as output:
        output.write(line + '\n')

### frequency swap ### 
#sweep 5 equally spaced frequency points in log scale from [start, start * 10)
def freqSweep(start,sens,initWaitTime):
    listOfFreq = np.zeros(5)
    for i in np.arange(0,5,1):
        listOfFreq[i] = start * 10**(0.2*i)
    for i in listOfFreq:
        lockin1.write('FREQ %f' %i)
        if (start < 1):
            error = 0.01
            sleep = 20#waiting for freq sync
        else:
            error = 1
            sleep = 5
        freq1 = float(lockin1.query('freq?'))
        freq2 = float(lockin2.query('freq?'))
        while (np.abs(i - freq1) > error or np.abs(i - freq2) > error):
            time.sleep(sleep)
            freq1 = float(lockin1.query('freq?'))
            freq2 = float(lockin2.query('freq?'))
        #print(i,freq1,freq2)
        measurement(freq1,freq2,sens,initWaitTime)
#single freq measurement for f > 1kHz      
def freqSweepSingle(start, sens,initWaitTime):
        lockin1.write('FREQ %f' %start)
        if (start < 1):
            error = 0.01
            sleep = 55#waiting for freq sync
        else:
            error = 1
            sleep = 5#waiting for freq sync
        freq1 = float(lockin1.query('freq?'))
        freq2 = float(lockin2.query('freq?'))
        while (np.abs(start - freq1) > error or np.abs(start - freq2) > error):
            time.sleep(sleep)
            freq1 = float(lockin1.query('freq?'))
            freq2 = float(lockin2.query('freq?'))
        #print(i,freq1,freq2)
        measurement(freq1,freq2,sens,initWaitTime)
      
        

####1w  measurement
#freq0 = 23
#sens = 0.001e-3
#lockin1.write('FREQ %d' %freq0)
#lockinInit_1w()
###set source voltage
#lockin1.write("SLVL 3")
##output.write("1w voltages:\n")
#f1 = float(freq0)
#f2 = float(freq0)
#time.sleep(2)
#X1 = float(lockin1.query("OUTP?1"))
#Y1 = float(lockin1.query("OUTP?2"))
#X2 = float(lockin2.query("OUTP?1"))
#Y2 = float(lockin2.query("OUTP?2"))
##    #check reading to be stable
#while (np.abs(X1 - float(lockin1.query('OUTP?1')))> sens
#    or np.abs(X2 - float(lockin2.query('OUTP?1')))> sens):
#    time.sleep(0.5)
#    X1 = float(lockin1.query("OUTP?1"))
#    Y1 = float(lockin1.query("OUTP?2"))
#    X2 = float(lockin2.query("OUTP?1"))
#    Y2 = float(lockin2.query("OUTP?2"))
#t = float(time.clock()-t0)
#line = str(t) + " " + str(f1) + " " + str(f2) + " "  \
#        + str(X1) + " " + str(Y1) + " "  \
#        + str(X2) + " " + str(Y2) + " " + str(datetime.now())
#print(line)
##output.write("end of 1w mesurement\n")
#lockin1.write("SLVL 0.004")

##3w measurement
lockinInit_3w()
#fg.write("FUNC 0")
#fg.write("AMPL0.315VR") #number is output voltage
#fg.write("OUTE1") # fg output on


lockin1.write("SLVL 1.8")

##freq sweep 0.001-0.01Hz
#timeCon = 17#
#sensitivity = 17# 18 FOR 2V; 14#100 UV;
#lockin_set_pms(timeCon,sensitivity)
#sens = 1e-7
#waitTime = 10*60#s
#freqSweep(0.1,sens,waitTime)

#freq sweep 0.01-0.1Hz
timeCon = 15#
sensitivity = 17# 18 FOR 2V; 14#100 UV;
lockin_set_pms(timeCon,sensitivity)
sens = 1e-7
waitTime = 30*60#s
freqSweep(0.1,sens,waitTime)

#freq sweep 0.1-1Hz
timeCon = 13#
sensitivity = 17# 18 FOR 2V; 14#100 UV;
lockin_set_pms(timeCon,sensitivity)
sens = 1e-7
waitTime = 10*60#s
freqSweep(0.1,sens,waitTime)

##freq sweep 1-10Hz
#timeCon =  13#
#sensitivity = 16#2mV
#lockin_set_pms(timeCon,sensitivity)
#sens = 1e-7#0.1e-3V
#waitTime = 5*60#s
#freqSweep(1,sens,waitTime)
#
##freq sweep 10-100Hz
#timeCon = 12#
#sensitivity = 16#500uV
#lockin_set_pms(timeCon,sensitivity)
#sens = 1e-7#0.01e-3#V
#waitTime = 5*60#s
#freqSweep(10,sens,waitTime)
#
##freq sweep 100-1000Hz
#timeCon = 11#
#sensitivity = 16# 500 uV
#lockin_set_pms(timeCon, sensitivity)
##lockinsingle_set_pms(lockin2, timeCon, 25)
#sens = 1e-7#0.001e-3#V
#waitTime = 5*60#s
#freqSweep(100,sens,waitTime)
#
##freq sweep 1000-10000Hz
#timeCon = 7#0.3s
#sensitivity = 16#0.2mV
#lockin_set_pms(timeCon,sensitivity)
#sens = 1e-7#V
#waitTime = 3*60#s
#freqSweep(1000,sens,waitTime)
#
##freq sweep for f>10KHz
#timeCon = 7#0.3s
#sensitivity = 16#0.2mV
#lockin_set_pms(timeCon,sensitivity)
#sens = 1e-7#V
#waitTime = 3*60#s
#freqSweepSingle(10000, sens, waitTime)
#freqSweepSingle(15000, sens, waitTime)
#freqSweepSingle(20000, sens, waitTime)
#freqSweepSingle(25000, sens, waitTime)
#freqSweepSingle(30000, sens, waitTime)
#
lockin1.write('freq 17')
lockin1.write("SLVL 0.004")
lockinInit_1w()
#fg.write("OUTE0") #fg output off
#C
output.close()# may record unfinished data
tf = datetime.now()
print ("Program done! total time is: "+ str(tf-ti))
