# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:43:38 2019

@author: Administrator
"""

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
rtdr = rm.open_resource('GPIB2::2::INSTR')
samp = rm.open_resource('GPIB2::15::INSTR')

date = '200708'
try:
    os.mkdir(date)
except FileExistsError:
    pass
TESTNAME = f"{date}//{date}_Bi2Te3_p2_seebeck_2.txt"
with open(TESTNAME, "w") as output:
    output.write("Date Time RTDl RTDr Vsamp\n")

ti = dt.datetime.now()
try:
    while True:
        ans1 = float( rtdl.query(":sens:data:fres?"))
        ans2 = float( rtdr.query(":sens:data:fres?"))
#        ans3 = float( samp.query("OUTP?1"))
#        ans4 = float( samp.query("OUTP?1")) / I
        ans3 = float(samp.query("sens:data:fres?"))
        line = str(dt.datetime.now()) + " " \
                     + str(ans1) + " "  \
                     + str(ans2) +  " "  \
                     + str(ans3) #+  " "  \
#                     + str(ans4)
        with open(TESTNAME, "a") as output:
            output.write(line + "\n")
        print(line)
except KeyboardInterrupt:  
    pass

output.close()
tf = dt.datetime.now()
print ("Program done! total time is: "+ str(tf-ti))

