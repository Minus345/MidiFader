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
    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.signals = WorkerSignals()
        self.is_killed = False

    @pyqtSlot()
    def run(self):
        while True:
            # time.sleep(1)
            line = str(serialInput.getLine(self.ser))
            self.signals.progress.emit(line)

            if self.is_killed:
                serialInput.killSerial(self.ser)
                break

    def kill(self):
        print("killed")
        self.is_killed = True
