from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from PythonSoftware.SerialToMidi.SerialLink import serialInput

class MidiWorkerSignals(QObject):
    progress = pyqtSignal(object)


class MidiWorker(QRunnable):

    def __init__(self):
        super().__init__()

        self.signals = MidiWorkerSignals()
        self.is_killed = False

    @pyqtSlot()
    def run(self):
        while True:
            print("hi")
            #self.signals.progress.emit("Running")
            if self.is_killed:

                break

    def kill(self):
        print("killed")
        self.is_killed = True
