#-------------------------------------------------------------------------------
# Name:        update speed test script for Maynuo eload
#              Generates a square wave to help testing the register write delay
# Purpose:
#
# Author:      Derryn Harvie
#
# Created:     16/04/2014
# Licence:     Public Domain
#-------------------------------------------------------------------------------

import Maynuo, time, sys

def main():

    #----------------------------------------------------------
    # This is the time delay after a register is written to the
    # load, that the internal microcontroller has to process
    # the write.  4ms is the shortest delay found to be reliable.
    #----------------------------------------------------------
    testRegisterWriteDelay = 0.004

    highCurrent = 2.0
    lowCurrent = 1.0

    load = Maynuo.Maynuo(19,115200,1,testRegisterWriteDelay)
    load.setCCurrent(lowCurrent)
    load.setInputOn()
    time.sleep(0.1)

    print('System speed test')

    currentHigh = False
    for i in range(0,100):
        if(currentHigh == False):
            load.setCCurrent(lowCurrent)
            currentHigh = True
        else:
            load.setCCurrent(highCurrent)
            currentHigh = False


    load.setInputOff()
if __name__ == '__main__':
    main()
