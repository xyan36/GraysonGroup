# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 12:09:07 2018

@author: Administrator
"""

import datetime as dt
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import visa
import os

rm = visa.ResourceManager()
rm.list_resources()
rtdl = rm.open_resource('GPIB2::1::INSTR')
#rtdr = rm.open_resource('GPIB2::1::INSTR')
samp = rm.open_resource('GPIB2::15::INSTR')
#fg = rm.open_resource('GPIB0::11::INSTR')
def init():
    #mm1.write("*RST");
    #mm1.write("SYST:BEEP:STAT OFF")
    rtdl.write(":SENS:FUNC 'RES'")
#    rtdr.write(":SENS:FUNC 'RES'")
    #samp.write(":SENS:FUNC 'FRES'")
### basic parameters ###
date = '201218'
try:
    os.mkdir(date)
except FileExistsError:
    pass    

FILENAME = date + '//' + date + '_' +"glass_R78_temp_coeff_DMM_dry_ice_2_heating_up.txt"

#output = open(FILENAME,"w");
with open(FILENAME, "w") as output:
    output.write("Date_Time,RTD,Rsamp\n")

#init();
##use fg to give a 5V DC heating
#fg.write("FUNC 0")
#fg.write('ampl0vr')
#fg.write('offs 5')
#fg.write("OUTE1") # fg output on

ti = dt.datetime.now()

#constants
#samp.write('SLVL2.276')
#V = 2.276 #lockin voltage
#Rref = 310.9e3 #large resistor to convert to current source
#I = V/Rref

try:
    while True:
        ans1 = float( rtdl.query(":sens:data:fres?"))
#        ans2 = float( rtdr.query(":sens:data:fres?"))
#        ans3 = float( samp.query("OUTP?1"))
#        ans4 = float( samp.query("OUTP?1")) / I
        ans2 = float(samp.query("sens:data:fres?"))
        line = str(dt.datetime.now()) + "," \
                     + str(ans1) + ","  \
                     + str(ans2)\
#                     + str(ans3) #+  " "  \
#                     + str(ans4)
        with open(FILENAME, "a") as output:             
            output.write(line + "\n")
        print(line)
        time.sleep(0.5)
except KeyboardInterrupt:  
    pass

finally:
    tf = dt.datetime.now()
    print ("Program done! total time is: "+ str(tf-ti))

