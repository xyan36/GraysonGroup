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
### basic parameters ###
date = '200310'
try:
    os.mkdir(date)
except FileExistsError:
    pass    
FILENAME = date + '//' + date + '_' +"glass_R43_3w_measurement_1.txt"
rm = visa.ResourceManager();
print(rm.list_resources())
#fg = rm.open_resource("GPIB::11::INSTR")
lockin1 = rm.open_resource("GPIB2::9::INSTR") #sample
lockin2 = rm.open_resource("GPIB2::18::INSTR") #reference resistor
lockin1.write("*cls")
lockin2.write("*cls")
t0 = time.time()

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

###1w  measurement
output1w = open(FILENAME[:-4] + '_1w.txt', 'w')
header = "Date_time Time TC SENS Lockin1f Lockin2f X1 Y1 X1_ref Y1_ref\n"
freq0 = 23
sens = 0.001e-3
timeCon = 9
sensitivity = 22
lockinsingle_set_pms(lockin1, timeCon, sensitivity)
lockinsingle_set_pms(lockin2, timeCon, sensitivity)
lockin1.write('FREQ %d' %freq0)
lockinInit_1w()
##set source voltage
Vs = 3;
lockin1.write("SLVL %d" %Vs)
output1w.write("1w input voltage: %d V\n" %Vs)
output1w.write(header)
f1 = float(freq0)
f2 = float(freq0)
time.sleep(10)
X1 = float(lockin1.query("OUTP?1"))
Y1 = float(lockin1.query("OUTP?2"))
X2 = float(lockin2.query("OUTP?1"))
Y2 = float(lockin2.query("OUTP?2"))
#    #check reading to be stable
while (np.abs(X1 - float(lockin1.query('OUTP?1')))> sens
    or np.abs(X2 - float(lockin2.query('OUTP?1')))> sens):
    time.sleep(0.5)
    X1 = float(lockin1.query("OUTP?1"))
    Y1 = float(lockin1.query("OUTP?2"))
    X2 = float(lockin2.query("OUTP?1"))
    Y2 = float(lockin2.query("OUTP?2"))
timeCon = int(lockin1.query('OFLT?'))
SENS = int(lockin1.query('SENS?'))
t = float(time.time()-t0)
line = str(datetime.now()) + str(t) + " " + str(timeCon) + " " + \
        str(SENS) + " " + str(f1) + " " + str(f2) + " "  \
        + str(X1) + " " + str(Y1) + " "  \
        + str(X2) + " " + str(Y2)
print(line)
output1w.write(line)
lockin1.write("SLVL 0.004")
print("End of 1w measurement")