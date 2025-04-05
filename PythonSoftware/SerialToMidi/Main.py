print("starting")

import serial
ser = serial.Serial('COM4')
print(ser.name)
line = ser.readline()
print(line)
ser.close()