from time import sleep

import mido
class Midi:
    def __init__(self,port):
        self.port = mido.open_output(port)
        self.running = True

    def sendMid(self,note,velocity):
        msg = mido.Message('note_on', note=note, velocity=velocity)
        self.port.send(msg)

    def closePort(self):
       self.port.close()


def getOpenMidiPort():
    return mido.get_output_names()