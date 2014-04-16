#-------------------------------------------------------------------------------
# Name:        IV tracking test script for Maynuo eload
# Purpose:
#
# Author:      Derryn Harvie
#
# Created:     16/04/2014
# Licence:     Public Domain
#-------------------------------------------------------------------------------

import Maynuo, time, sys

def main():
    startCurrent = 0.0
    stopCurrent = 1.0
    stepCurrent = 0.01
    stepDelayTime = 0.5

    testCurrent = startCurrent

    load = Maynuo.Maynuo(19,57600,1)
    load.setCCurrent(testCurrent)
    load.setInputOn()
    time.sleep(stepDelayTime)

    print('System Test')
    print('Time (ms), Voltage (V), Current (A)')

    while(1):
    # get the operating point and write out
        opPoint = load.getOperatingPoint()
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
if __name__ == '__main__':
    main()
