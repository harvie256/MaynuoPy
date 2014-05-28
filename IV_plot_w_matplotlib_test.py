#-------------------------------------------------------------------------------
# Name:        IV ploting test script for Maynuo eload using Matplotlib
# Purpose:
#
# Author:      Derryn Harvie
#
# Created:     16/04/2014
# Licence:     Public Domain
#-------------------------------------------------------------------------------

import Maynuo, time, sys
import matplotlib.pyplot as plt

def main():
    startCurrent = 0.0
    stopCurrent = 4.60
    stepCurrent = 0.01
    stepDelayTime = 0.5

    testCurrent = startCurrent
    I_List = []
    V_List = []

    load = Maynuo.Maynuo(19,57600,1)
    load.setCCurrent(testCurrent)
    load.setInputOn()
    time.sleep(stepDelayTime)

    print('System Test')
    print('Time (ms), Voltage (V), Current (A)')

    while(1):
    # get the operating point and write out
        opPoint = load.getOperatingPoint()
        I_List.append(opPoint.getCurrent())
        V_List.append(opPoint.getVoltage())
        sys.stdout.write(str(int(round(time.time() * 1000))) + ', ')
        sys.stdout.write("{0:.4f}".format(opPoint.getVoltage()) + ', ')
        print("{0:.4f}".format(opPoint.getCurrent()))
    # step the current and test for ending
        testCurrent += stepCurrent
        if(testCurrent > stopCurrent):
            break
        load.setCCurrent(testCurrent)
        time.sleep(stepDelayTime)

    load.setInputOff()
    print('IV sweep complete')

    plt.plot(I_List,V_List,'r-')
    plt.title('85W magsafe charger (18.5V @ 4.6A rated)')
    plt.xlabel('Current (A)')
    plt.ylabel('Voltage (V)')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
