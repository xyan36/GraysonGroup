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
rtdl = rm.open_resource('GPIB2::15::INSTR') #21 23
rtdr = rm.open_resource('GPIB2::1::INSTR')#14 15
samp = rm.open_resource('GPIB2::2::INSTR')  

date = '210701'
try:
    os.mkdir(date)
except FileExistsError:
    pass    
FILENAME = date + '//' + date + '_' +"Bi2Te3_p11_2mm_temp_coeff_test_1.txt"
header = "Date_Time,RTDl,RTDr,Rsamp\n"
with open(FILENAME, "w") as output:
    output.write(header)
print(header)

ti = dt.datetime.now()
try:
    while True:
        ans1 = float( rtdl.query(":sens:data:fres?"))
        ans2 = float( rtdr.query(":sens:data:fres?"))
        ans3 = float(samp.query("sens:data:fres?"))
        line = str(dt.datetime.now()) + "," \
                     + str(ans1) + ","  \
                     + str(ans2) +  ","  \
                     + str(ans3)
        with open(FILENAME, "a") as output:             
            output.write(line + "\n")
        print(line)
        time.sleep(0.1)
except KeyboardInterrupt:  
    pass
finally:
    tf = dt.datetime.now()
    print ("Program done! total time is: "+ str(tf-ti))

