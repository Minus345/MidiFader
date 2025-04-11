import sys
from multiprocessing.pool import worker

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool

import serialInput
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QRadioButton, QLabel, QVBoxLayout, QWidget, \
    QButtonGroup, QLineEdit, QHBoxLayout

from PythonSoftware.SerialToMidi.faderClass import Fader
from PythonSoftware.SerialToMidi.multithreading import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.setWindowTitle("Serial To Midi")
        self.setMinimumWidth(500)

        self.layout = QVBoxLayout()

        self.startButton = QPushButton("Start Encoding")
        self.startButton.clicked.connect(self.startButtonPressed)
        self.layout.addWidget(self.startButton)

        self.comInput = QLineEdit()
        self.comPort = "Com4"  # default for my testing
        self.comInput.setPlaceholderText("Input Com Port")
        self.comInput.textChanged.connect(self.comInputChanged)
        self.layout.addWidget(self.comInput)

        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.stopButtonPress)
        self.layout.addWidget(self.stopButton)

        self.dataFromFader = QLabel("Input")
        self.layout.addWidget(self.dataFromFader)

        # ----- Fader ----------
        # creates 8 Labels horizontally
        self.faderList = [Fader] * 12

        self.layout2 = QHBoxLayout()

        for x in range(12):
            self.faderList[x] = Fader(x, self.layout2)

        self.faderUiElement = QWidget()
        self.faderUiElement.setLayout(self.layout2)

        # -----------------------

        self.layout.addWidget(self.faderUiElement)

        self.maineUiElement = QWidget()
        self.maineUiElement.setLayout(self.layout)
        self.setCentralWidget(self.maineUiElement)
        self.show()

        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")

    def startButtonPressed(self):

        # If this returns False the Serial Port is not found
        usedSetup = serialInput.setup(self.comPort)

        if usedSetup is False:
            return

        self.worker = Worker(usedSetup)
        self.worker.signals.finished.connect(self.thread_complete)
        self.worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(self.worker)

    # Input for the Com Port (Windows)
    def comInputChanged(self, s):
        print(s)
        self.comPort = s

    # Stopps the running Serial Connection
    def stopButtonPress(self):
        if self.worker:
            self.worker.kill()
        else:
            print("No thread started")

    # Verbindung zu Signals für das GUI
    def progress_fn(self, n):
        n = n.replace("b'", "")
        n = n.replace("\\r\\n'", "")

        # splits the string and sends it to the display labels
        split = n.split("|")
        if len(split) >= 12:
            for x in range(12):
                self.faderList[x].updateData(round(int(split[x]), -1)) # runden auf nächsten 10
                self.dataFromFader.setText(str(n))

    def thread_complete(self):
        print("THREAD COMPLETE!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
