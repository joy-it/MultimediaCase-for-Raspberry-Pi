#!/usr/bin/env python
import serial
import os

ser = serial.Serial(
	port='/dev/serial0',
	baudrate = 38400,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

counter=0

ser.write(str.encode('\x0D'))
ser.write(str.encode('X05'))
ser.write(str.encode('\x0D'))

while 1:
	x=ser.readline()
	y = x.decode(encoding='UTF-8',errors='strict')
	if y==('xxxShutdownRaspberryPixxx\n'):
		print ("Raspberry Pi Shutdown")
		os.system("sudo shutdown -h now")
