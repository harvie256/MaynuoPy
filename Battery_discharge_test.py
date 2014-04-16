#-------------------------------------------------------------------------------
# Name:        Battery constant power discharge test script
# Purpose:
#
# Author:      Derryn Harvie
#
# Created:     16/04/2014
# Licence:     Public Domain
#-------------------------------------------------------------------------------
import Maynuo, time, sys
from decimal import *

dischargePower = 2.5
stopVoltage = 3.1
stepDelayTime = 0.5
filename = "C:/temp/testFile.csv"


def getMillis():
    return int(round(time.time() * 1000))

def main():

    def printAndWrite(fileToWrite, string):
        fileToWrite.write(string + '\n')
        print(string)

    f = open(filename, 'w')

    load = Maynuo.Maynuo(19,57600,1)
    load.setCPower(dischargePower)
    load.setInputOn()
    endMillis = startMillis = getMillis()

    printAndWrite(f, 'Battery discharge Test @ ' + str(dischargePower))
    printAndWrite(f, 'Time (ms), Voltage (V), Current (A)')

    while(1):
    # get the operating point and write out
        opPoint = load.getOperatingPoint()
        currentMillis = getMillis() - startMillis
        printAndWrite(f, str(currentMillis) + ', ' + "{0:.4f}".format(opPoint.getVoltage()) + ', ' + "{0:.4f}".format(opPoint.getCurrent()))
    # test the voltage for the battery cutout voltage
        if(opPoint.getVoltage() < stopVoltage):
            endMillis = currentMillis
            break
        time.sleep(stepDelayTime)

    load.setInputOff()
    print("*** Battery test complete ***")
    power = dischargePower * (endMillis/ (1000.0 * 60 * 60))
    print("Total power = " + "{0:.4f}".format(power) + 'Wh')
    f.close()

if __name__ == '__main__':
    main()
