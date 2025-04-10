import serial

def setup(comPort):
    try:
        ser = serial.Serial(comPort)
        print(ser.name)
    except serial.SerialException as e:
        print(e)
        ser = False
    return ser

def getLine(ser):
    line = ser.readline()
    print(line)
    return line

def killSerial(ser):
    ser.close()
