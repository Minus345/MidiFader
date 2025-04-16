from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from PythonSoftware.SerialToMidi.RunningThreads.faderData import FaderData
from PythonSoftware.SerialToMidi.SerialLink import serialInput


class WorkerSignals(QObject):
    progress = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, ser, midi, faders):
        super().__init__()
        self.ser = ser
        self.midi = midi

        # extract data out of Fader from UI
        self.faderStorage = [FaderData] * 12
        for x in range(12):
            self.faderStorage[x] = FaderData(x)

        self.signals = WorkerSignals()
        self.is_killed = False

    @pyqtSlot()
    def run(self):
        while True:
            line = str(serialInput.getLine(self.ser))
            line = line.replace("b'", "")
            line = line.replace("\\r\\n'", "")

            # splits the string
            split = line.split("|")
            if len(split) >= 12:
                self.signals.progress.emit(split)
                for x in range(12):
                    self.faderStorage[x].data = split[x]
                    v = ((int(self.faderStorage[x].data)) / 1024) * 127
                    self.midi.sendMid(self.faderStorage[x].midiNote, round(v))

            if self.is_killed:
                serialInput.killSerial(self.ser)
                self.midi.closePort()
                break

    def kill(self):
        print("killed")
        self.is_killed = True
