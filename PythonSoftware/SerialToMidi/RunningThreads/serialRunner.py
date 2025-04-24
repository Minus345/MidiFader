from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from PythonSoftware.SerialToMidi.SerialLink import serialInput


class WorkerSignals(QObject):
    progress = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, ser, midi, faders):
        super().__init__()
        self.ser = ser
        self.midi = midi
        self.faders = faders

        self.signals = WorkerSignals()
        self.is_killed = False

    @pyqtSlot()
    def run(self):

        oldFaderData = [0] * 12

        while True:
            line = str(serialInput.getLine(self.ser))
            line = line.replace("b'", "")
            line = line.replace("\\r\\n'", "")

            # splits the string
            split = line.split("|")
            if len(split) >= 12:
                self.signals.progress.emit(split)
                for x in range(12):
                    self.faders[x].data = split[x]
                    v = round(((int(self.faders[x].data)) / 1024) * 127)

                    if v != oldFaderData[x]:
                        self.midi.sendMid(self.faders[x].faderObjekt.midiNote, v)

            for x in range(12):
                oldFaderData[x] = round(((int(self.faders[x].data)) / 1024) * 127)

            if self.is_killed:
                serialInput.killSerial(self.ser)
                self.midi.closePort()
                break

    def kill(self):
        print("killed")
        self.is_killed = True
