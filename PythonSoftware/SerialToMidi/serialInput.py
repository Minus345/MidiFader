#print("starting")
import serial
def setup():
    ser = serial.Serial('COM4')
    print(ser.name)
    return ser

def getLine(ser):
    line = ser.readline()
    print(line)
    return line

def killSerial(ser):
    ser.close()
