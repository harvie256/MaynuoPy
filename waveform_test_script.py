#-------------------------------------------------------------------------------
# Name:        output a waveform as fast as possible
#                test script for Maynuo eload
# Purpose:
#
# Author:      Derryn Harvie
#
# Created:     16/04/2014
# Licence:     Public Domain
#-------------------------------------------------------------------------------

import Maynuo, time, sys, math

pi = 3.14159265358

def main():

    #----------------------------------------------------------
    # This is the time delay after a register is written to the
    # load, that the internal microcontroller has to process
    # the write.  4ms is the shortest delay found to be reliable.
    #----------------------------------------------------------
    testRegisterWriteDelay = 0.004

    #----------------------------------------------------------
    # Generate the wave array based on the register update time
    #----------------------------------------------------------
    scale = 1.0
    offset = 1.0
    freq = 1.0

    numberOfPoints = int(freq / (testRegisterWriteDelay * 2))
    print ("Frequency: " + str(freq) + " Data Points: " + str(numberOfPoints))
    waveList = []
    for x in range(0, numberOfPoints):
        point = math.sin((x * 2.0 * pi) / numberOfPoints) * (scale) + offset
        waveList.append(point)


    load = Maynuo.Maynuo(19,115200,1,testRegisterWriteDelay)
    load.setCCurrent(waveList[0])
    load.setInputOn()
    time.sleep(0.1)

    #----------------------------------------------------------
    # Continuously loops through the array changing the current
    #----------------------------------------------------------
    while(True):
        for i in range(0,len(waveList)):
            load.setCCurrent(waveList[i])

    load.setInputOff()
if __name__ == '__main__':
    main()
