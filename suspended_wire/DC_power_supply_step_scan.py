#DC POWER SUPPLY Agilent E3631A
import numpy as np
import time
def init():
    dc.write("INST P6V")
    dc.write("CURR 1.0")

def voltageScan(timeSleep, voltage):
  time.sleep(timeSleep);
  dc.write("VOLT %f" %voltage)

steps = np.arange(0,11,1) #numbre of steps of a scan
dt = 60 #time interval between each step
c = 0.013 #define a constant

init()
#heating steps
for step in steps:
    voltageScan(timeSleep = dt, voltage = c * np.sqrt(step*dt))
time.sleep(5*60);
#cooling steps
for step in np.flip(steps,0):
    voltageScan(timeSleep = dt, voltage = c * np.sqrt(step*dt))
