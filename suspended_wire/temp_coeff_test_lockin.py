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
rtdl = rm.open_resource('GPIB2::2::INSTR')
rtdr = rm.open_resource('GPIB2::1::INSTR')
lockin1 = rm.open_resource('GPIB2::9::INSTR') #sample
lockin2 = rm.open_resource('GPIB2::18::INSTR') #reference

date = '200625'
try:
    os.mkdir(date)
except FileExistsError:
    pass    
FILENAME = date + '//' + date + '_' +"Bi2Te30617_temp_coeff_test1.txt"
header = "Date Time RTDl RTDr Vsamp Vref\n"
with open(FILENAME, "w") as output:
    output.write(header)
print(header)

lockin1.write('slvl 1.1')
ti = dt.datetime.now()
try:
    while True:
        ans1 = float( rtdl.query(":sens:data:fres?"))
        ans2 = float( rtdr.query(":sens:data:fres?"))
        ans3 = float( lockin1.query("OUTP?1"))
        ans4 = float( lockin2.query("OUTP?1"))
        line = str(dt.datetime.now()) + " " \
                     + str(ans1) + " "  \
                     + str(ans2) +  " "  \
                     + str(ans3) +  " "  \
                     + str(ans4)
        with open(FILENAME, "a") as output:             
            output.write(line + "\n")
        print(line)
        time.sleep(0.5)
except KeyboardInterrupt:  
    pass
finally:
    lockin1.write('slvl 0.004')
    tf = dt.datetime.now()
    print ("Program done! total time is: "+ str(tf-ti))


