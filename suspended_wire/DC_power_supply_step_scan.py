#DC POWER SUPPLY Agilent E3631A
import numpy as np
import time
def init():
    dc.write("INST P6V")
    dc.write("CURR 1.0")

def voltageScan(timeSleep, voltage):
  time.sleep(timeSleep);
  dc.write("VOLT %f" %voltage)

#init()
#heating steps
upVoltages = np.arange(0.2, 1.4, 0.2)
for voltage in upVoltages:
    voltageScan(120, voltage)

#cooling steps
downVoltages = np.arange(1.2, -0.4, -0.2)
for voltage in downVoltages:
    voltageScan(120, voltage)
