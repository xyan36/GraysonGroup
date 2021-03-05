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
s1 = rm.open_resource('GPIB2::15::INSTR')
s2 = rm.open_resource('GPIB2::1::INSTR')
s3 = rm.open_resource('GPIB2::2::INSTR')
#s4 = rm.open_resource('GPIB2::16::INSTR')  

date = '210304'
try:
    os.mkdir(date)
except FileExistsError:
    pass    
FILENAME = date + '//' + date + '_' +"Bi2Te3_p5_contact_test4.txt"
header = "Date_Time,RTDl,RTDr,Rsamp\n"
with open(FILENAME, "w") as output:
    output.write(header)
print(header)

ti = dt.datetime.now()
try:
    while True:
        ans1 = float( s1.query(":sens:data:fres?"))
        ans2 = float( s2.query(":sens:data:fres?"))
        ans3 = float(s3.query("sens:data:fres?"))
#        ans4 = float(s4.query("sens:data:fres?"))
        line = str(dt.datetime.now()) + "," \
                     + str(ans1) + ","  \
                     + str(ans2) +  ","  \
                     + str(ans3) #+  ","  \
#                     + str(ans4)
        with open(FILENAME, "a") as output:             
            output.write(line + "\n")
        print(line)
        time.sleep(10)
except KeyboardInterrupt:  
    pass
finally:
    tf = dt.datetime.now()
    print ("Program done! total time is: "+ str(tf-ti))

