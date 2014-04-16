#-------------------------------------------------------------------------------
# Name:        Maynuo M9710 python control library
# Purpose:
#
# Author:      Derryn Harvie
#
# Created:     15/04/2014
# Licence:     Public Domain
#-------------------------------------------------------------------------------

import crcmodbus, serial
import struct, time
from array import array

class OperatingPoint:
    def __init__(self, voltage=0, current=0):
        self.voltage = voltage
        self.current = current
    def getCurrent(self):
        return self.current
    def getVoltage(self):
        return self.voltage
    def setVoltage(self,voltage):
        self.voltage = voltage
    def setCurrent(self, current):
        self.current = current


class Maynuo:

    def __init__(self, serial_port, serial_baud, slave_address):
        self.commPort = serial.Serial(serial_port, serial_baud, timeout=1)
        self.slaveAddress = chr(slave_address)

    def addCRC(self, pack):
        crc = crcmodbus.INITIAL_MODBUS
        for ch in pack:
            crc = crcmodbus.calcByte( ch, crc)
        crc1 = crc & 0xFF
        crc2 = crc >> 8
        comWithCRC = pack + chr(crc1) + chr(crc2)
        return comWithCRC

    def writeRegister(self, startAddress, data):
        packet = self.slaveAddress
        adr1 = startAddress >> 8
        adr2 = startAddress & 0xFF
        noOfBytes = len(data)
        noOfReg = len(data)/2
        packet += ''.join(chr(x) for x in [0x10, adr1, adr2, 0x00, noOfReg, noOfBytes])
        packet += data
        packetWithCRC = self.addCRC(packet)
        self.commPort.write(packetWithCRC)
        time.sleep(0.05)

    def getOperatingPoint(self):
        packet = self.slaveAddress
        packet += ''.join(chr(x) for x in [0x03, 0x0B, 0x00, 0x00, 0x04])
        packetWithCRC = self.addCRC(packet)
        self.commPort.flushInput()
        self.commPort.write(packetWithCRC)
        ret = self.commPort.read(3)
        numberOfBytes = ord(ret[2]) + 2
        ret = self.commPort.read(numberOfBytes)

        floatStr = ret[0:4]
        voltage = struct.unpack('f', floatStr[::-1])
        floatStr = ret[4:8]
        current = struct.unpack('f', floatStr[::-1])

        return OperatingPoint(voltage[0],current[0])

    def setCurrent(self, current=0):
        valueAsStr = struct.pack('f', current)
        data = valueAsStr[::-1]
        self.writeRegister(0x0A01,data)
        command = ''.join(chr(x) for x in [0x00, 0x01])
        self.writeRegister(0x0A00, command)

    def setInputOn(self):
        command = ''.join(chr(x) for x in [0x00, 42])
        self.writeRegister(0x0A00,command)

    def setInputOff(self):
        command = ''.join(chr(x) for x in [0x00, 43])
        self.writeRegister(0x0A00,command)


