from time import sleep

import mido

def midi():
    print(mido.get_output_names())
    port = mido.open_output('midi 2')
    while True:
        #sleep(1)
        x = input("a")
        msg = mido.Message('note_on', note=60, velocity=int(x))
        port.send(msg)

def getOpenMidiPort():
    return mido.get_output_names()