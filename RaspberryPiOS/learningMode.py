#!/usr/bin/env python
import serial
import os
import time

ser = serial.Serial(
	port='/dev/serial0',
	baudrate = 38400,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

ser.write(str.encode('\x0D'))
ser.write(str.encode('X04'))
ser.write(str.encode('\x0D'))
time.sleep(.1)
ser.write(str.encode('000\r'))
