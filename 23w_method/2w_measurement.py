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
date = '200303'
try:
    os.mkdir(date)
except FileExistsError:
    pass    

FILENAME = date + '//' + date + '_' +"glass_R43_R2019_2w_measurement_1.txt"

rm = visa.ResourceManager();
print(rm.list_resources())
#fg = rm.open_resource("GPIB::11::INSTR")
lockin1 = rm.open_resource("GPIB2::9::INSTR") #heater SINE OUT, therm 2w
lockin2 = rm.open_resource("GPIB2::18::INSTR") #heater 1w
lockin1.write("*cls")
lockin2.write("*cls")
#mm1 = rm.open_resource("GPIB::2::INSTR")
#lockin1.timeout = 25000
#lockin2.timeout = 25000

### output file initialize ###
#FILENAME = TESTNAME + '_' + str(datetime.now()).replace(':','-') + ".txt"
#output = open(FILENAME,'w')
t0 = time.time()
ti = datetime.now()
header = "Date_time Time TC SENS Lockin1f Lockin2f X2 Y2 X1 Y1\n"
with open(FILENAME, 'w') as output:
    output.write(header)

### lock in initialize ###
#def lockinInit_1w():
#    #set lockin1 to internal (1), lockin2 to external(0)
#    lockin1.write("FMOD 0")
#    lockin2.write("FMOD 0")
#    #set lockins to measure the 1w voltage
#    lockin1.write("HARM 1")
#    lockin2.write("HARM 1")
#    #make phases zero
#    lockin1.write("PHAS 0")
#    lockin2.write("PHAS 0")
#    #set input configuration
#    lockin1.write("ISRC 1")
#    lockin2.write("ISRC 1")
#    #ground type
#    lockin1.write("IGND 1")
#    lockin2.write("IGND 1")
#    #input coupling ac 0 dc 1
#    lockin1.write("ICPL 1")
#    lockin2.write("ICPL 1")
#    #reserve mode
#    lockin1.write("RMOD 1")
#    lockin2.write("RMOD 1")
#    #sensitivity
#    lockin1.write("SENS 22")
#    lockin2.write("SENS 22")
#    #time constant
#    lockin1.write("OFLT 9")
#    lockin2.write("OFLT 9")  
#def lockinInit_3w():
#    #set lockins to measure the 3w voltage
#    lockin1.write("HARM 3")
#    lockin2.write("HARM 3")
#    #reserve mode
#    lockin1.write("RMOD 1")
#    lockin2.write("RMOD 1")
def lockinInit_harmonics(lockin, num):
    #set lockins to measure the 2w voltage
    lockin.write("HARM %d" %num)
    #reserve mode
    lockin.write("RMOD 1")
#def lockin_set_pms(timeCon,sensitivity):
#    #time constant
#    lockin1.write("OFLT %d" %timeCon)
#    lockin2.write("OFLT %d" %timeCon)
#    #sensitivity
#    lockin1.write("SENS %d" %sensitivity)
#    lockin2.write("SENS %d" %sensitivity)
def lockinsingle_set_pms(lockin, timeCon, sensitivity):
    #time constant
    lockin.write("OFLT %d" %timeCon)
    #sensitivity
    lockin.write("SENS %d" %sensitivity)

### measurements ###
def measurement(f1,f2,sens,initWaitTime): #sens= allowed error in reading
    X1 = float(lockin1.query("OUTP?1"))
    Y1 = float(lockin1.query("OUTP?2"))
    X2 = float(lockin2.query("OUTP?1"))
    Y2 = float(lockin2.query("OUTP?2"))
    time.sleep(initWaitTime) #initial wait time
    X22 = float(lockin2.query("OUTP?1"))
    #check reading to be stable
    while np.abs(X2 - X22)> sens:
        X22 = float(lockin2.query("OUTP?1"))
#        Y22 = float(lockin2.query("OUTP?2"))
        time.sleep(5) #additional wait time
        X1 = float(lockin1.query("OUTP?1"))
        Y1 = float(lockin1.query("OUTP?2"))
        X2 = float(lockin2.query("OUTP?1"))
        Y2 = float(lockin2.query("OUTP?2"))     
    t = float(time.time()-t0)
    timeCon = lockin2.query('OFLT?').rstrip()
    SENS = lockin2.query('SENS?').rstrip()
    f1 = float(lockin1.query('freq?'))
    f2 = float(lockin2.query('freq?'))
    line = str(datetime.now()) + " " + str(t) + " " \
    + str(timeCon) + " " + str(SENS) + " "  \
    + str(f1) + " " + str(f2) + " "  \
    + str(X1) + " " + str(Y1) + " "  \
    + str(X2) + " " + str(Y2)
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
        
def freqSweep_range(start,end,step,sens,initWaitTime):
    listOfFreq = np.arange(start, end, step)
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

def freqSweep_log(start,end,numOfPts,sens,initWaitTime):
    listOfFreq = np.zeros(numOfPts)
    logstep = np.log(end / 10) / (numOfPts * np.log(10))
    for i in np.arange(0,numOfPts,1):
        listOfFreq[i] = start * 10**(logstep * i)
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
      
        
##initialize lockin1 to 1w for heater, lockin2 to 2w for thermometer
lockinInit_harmonics(lockin1, 2)
lockinInit_harmonics(lockin2, 1)
#Turn on DC power for thermometer (10V)
lockin1.write("SLVL 5")

try:
    ##freq sweep 0.001-0.01Hz
    #timeCon = 17#
    #sensitivity = 17# 18 FOR 2V; 14#100 UV;
    #lockin_set_pms(timeCon,sensitivity)
    #sens = 1e-7
    #waitTime = 10*60#s
    #freqSweep(0.1,sens,waitTime)
    
    ##freq sweep 0.01-0.1Hz
    #timeCon = 15#
    #sensitivity = 17# 18 FOR 2V; 14#100 UV;
    #lockin_set_pms(timeCon,sensitivity)
    #sens = 1e-7
    #waitTime = 30*60#s
    #freqSweep(0.01,sens,waitTime)
    
    ##freq sweep 0.1-1Hz
    #timeCon = 13#
    #sensitivity = 17# 18 FOR 2V; 14#100 UV;
    #lockin_set_pms(timeCon,sensitivity)
    #sens = 1e-7
    #waitTime = 10*60#s
    #freqSweep(0.1,sens,waitTime)
    
    ##freq sweep 1-10Hz
    #timeCon = 12#
    #sensitivity1 = 26#500uV
    #sensitivity2 = 16#500uV
    #sens = 1e-7#for 2w
    #waitTime = 2*60#s
    #lockinsingle_set_pms(lockin1, timeCon,sensitivity1)
    #lockinsingle_set_pms(lockin2, timeCon,sensitivity2)
    ##freqSweep(20,sens,waitTime)
    #freqSweep_range(1,10,1,sens,waitTime)
    
    #freq sweep 20-200Hz
    timeCon = 11#
    sensitivity1 = 16#500uV
    sensitivity2 = 26#500uV
    sens = 1e-7#for 2w
    waitTime = 1*60#s
    lockinsingle_set_pms(lockin1, timeCon,sensitivity1)
    lockinsingle_set_pms(lockin2, timeCon,sensitivity2)
    #freqSweep(20,sens,waitTime)
    freqSweep_log(10,2000,30,sens,waitTime)
    
    
#    #freq sweep 200-2000Hz
#    timeCon = 10#
#    sensitivity1 = 26#500uV
#    sensitivity2 = 16#500uV
#    sens = 1e-7#for 2w
#    waitTime = 3*60#s
#    lockinsingle_set_pms(lockin1, timeCon,sensitivity1)
#    lockinsingle_set_pms(lockin2, timeCon,sensitivity2)
#    #freqSweep(200,sens,waitTime)
#    freqSweep_range(101.57,2001.57,100,sens,waitTime)
    
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
except KeyboardInterrupt:
    pass
finally:
    lockin1.write('freq 17')
    lockin1.write("SLVL 0.004")
    #lockinInit_1w()
    #fg.write("OUTE0") #fg output off
    #C
    output.close()# may record unfinished data
    tf = datetime.now()
    print ("Program done! total time is: "+ str(tf-ti))
