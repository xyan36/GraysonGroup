# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 16:47:36 2020

@author: B145 Experiment2
"""
from datetime import datetime
import time
import visa
import numpy as np
import os

### lock in initialize ###

def lockinInit_1w():
#    #set lockin1 to internal (1), lockin2 to external(0)
#    lockin1.write("FMOD 0")
#    lockin2.write("FMOD 0")
    #set lockins to measure the 1w voltage
    lockin1.write("HARM 1")
    lockin2.write("HARM 1")
    #make phases zero
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
    lockin1.write("RMOD 1")
    lockin2.write("RMOD 1")
#    #sensitivity
#    lockin1.write("SENS 22")
#    lockin2.write("SENS 22")
#    #time constant
#    lockin1.write("OFLT 9")
#    lockin2.write("OFLT 9")  
    
def lockinsingle_set_pms(lockin, timeCon, sensitivity):
    #time constant
    lockin.write("OFLT %d" %timeCon)
    #sensitivity
    lockin.write("SENS %d" %sensitivity)   
    
### measurements ###
def measurement(f1,f2,sens,initWaitTime): #sens= allowed error in reading
    try:
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
        line = str(datetime.now()) +" " + str(t) + " " \
        + str(timeCon) + " " + str(SENS) + " "  \
        + str(f1) + " " + str(f2) + " "  \
        + str(X3) + " " + str(Y3) + " "  \
        + str(X3_ref) + " " + str(Y3_ref)
        print(line)
#        user = input('Record the readings? y/n: ')
#        while (user == 'n'):
#            print('Not recorded.')
#            user = input('Record the readings? y/n: ')
#        if (user == 'y'):
        with open(FILENAME, 'a') as output:
            output.write(line + '\n')
            print('Data Recorded.')
    except KeyboardInterrupt:
        print('Keyboard Interrupt.')
    finally:
        return
        
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

###1w  measurement ###
### basic parameters ###
date = '210630'
try:
    os.mkdir(date)
except FileExistsError:
    pass    
FILENAME = date + '//' + date + '_' +"Bi2Te3_p11_2mm_3w_1w_collection_1.txt"
header = "Date_time Time TC SENS Lockin1f Lockin2f X1 Y1 X1_ref Y1_ref\n"
rm = visa.ResourceManager();
print(rm.list_resources())
lockin1 = rm.open_resource("GPIB2::8::INSTR") #sample
lockin2 = rm.open_resource("GPIB2::9::INSTR") #reference resistor
lockin1.write("*cls")
lockin2.write("*cls")
t0 = time.time()
Vs = 0.9 #source voltage
freq = 17
sens = 0.001e-3 #allowed error in data
timeCon = 9
sensitivity = 24
initWaitime = 8 * 60

#lockinInit_1w()
lockin1.write("HARM 1")
lockin2.write("HARM 1")
lockinsingle_set_pms(lockin1, timeCon, sensitivity)
lockinsingle_set_pms(lockin2, timeCon, sensitivity)
lockin1.write("SLVL %f" %Vs)
lockin1.write('FREQ %f' %freq)
with open(FILENAME,'a') as output1w:
    output1w.write("1w input voltage: %f V\n" %Vs)
    output1w.write(header)

freqSweepSingle(freq, sens, initWaitime)

lockin1.write("SLVL 0.004")
print("End of 1w measurement")