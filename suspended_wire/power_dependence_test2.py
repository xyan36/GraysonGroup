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
    lockin1.write("HARM 1")
    lockin2.write("HARM 1")

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
    
def lockinsingle_set_pms(lockin, timeCon, sensitivity):
    #time constant
    lockin.write("OFLT %d" %timeCon)
    #sensitivity
    lockin.write("SENS %d" %sensitivity)
    
def outputs_query():
    X3 = lockin1.query('outp?1').rstrip()
    Y3 = lockin1.query('outp?2').rstrip()
    X1_ref = lockin2.query('outp?1').rstrip()
    Y1_ref = lockin2.query('outp?2').rstrip()
    header = "X3 Y3 X1_ref Y1_ref"
    print(header)
    print(X3, Y3, X1_ref, Y1_ref, sep = "\t")
def settings_query():
    f1 = lockin1.query('freq?').rstrip()
    f2 = lockin2.query('freq?').rstrip()
    tc1 = lockin1.query('oflt?').rstrip()
    tc2 = lockin2.query('oflt?').rstrip()
    sstvt1 = lockin1.query('sens?').rstrip()
    sstvt2 = lockin2.query('sens?').rstrip()
    header = "LOCKIN# FREQ TC SENS"
    print(header)
    print('lockin1', f1, tc1, sstvt1, sep = "\t")
    print('lockin2', f2, tc2, sstvt2, sep = "\t")
    
    
def set_V_input(lockin, voltage):
    lockin.write('slvl %f' %voltage)
    print(datetime.now(), f"Set V = {voltage}")

### measurements ###
def measurement(sens,initWaitTime, add_wait_time = 5): #sens= allowed error in reading
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
        time.sleep(add_wait_time) #additional wait time
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
date = '200708'
try:
    os.mkdir(date)
except FileExistsError:
    pass
FILENAME = f"{date}//{date}_Bi2Te3_p2_power_dep_f3p4.txt"

rm = visa.ResourceManager();
print(rm.list_resources())
lockin1 = rm.open_resource("GPIB2::9::INSTR") #sample & SINE_OUT source
lockin2 = rm.open_resource("GPIB2::18::INSTR") #reference resistor

header = "Date time Time V_input X3 Y3 X1_ref Y1_ref\n"
#with open(FILENAME,'w') as output:
#    output.write(header)

### Set the parameters ###
freq = 3.4 #Hz
timeCon = 14#100s
voltages = np.array([4, 4.5, 5])
sensitivity1 = 22#50mV  sensitivity for 1w measurement
sensitivity3 = 12#20uV  sensitivity for 3w measurement
initWaitTime = 15 * 60#s
lockin1.write('harm 3')
lockin2.write('harm 1')
##########################
lockin1.write('FREQ %f' %freq)
t0 = time.time()
ti = datetime.now()
lockinsingle_set_pms(lockin1, timeCon, sensitivity3)
lockinsingle_set_pms(lockin2, timeCon, sensitivity1)
try:
    for v in voltages:
        set_V_input(lockin1, v)
        time.sleep(initWaitTime)
        outputs_query()
except KeyboardInterrupt:
    print('keyboardinteeruupt')
    pass
lockin1.write("SLVL %f" %0.004)
#output.close()# may record unfinished data
tf = datetime.now()
print ("Program done! total time is: "+ str(tf-ti))
