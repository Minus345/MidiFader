import sys

from PyQt6.QtCore import QThreadPool

from PythonSoftware.SerialToMidi import midi
from PythonSoftware.SerialToMidi.SerialLink import serialInput
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, \
    QHBoxLayout, QComboBox

from PythonSoftware.SerialToMidi.SerialLink.serialPortDetection import serial_ports
from PythonSoftware.SerialToMidi.faderClass import Fader
from PythonSoftware.SerialToMidi.midi import Midi
from PythonSoftware.SerialToMidi.RunningThreads.serialRunner import Worker

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # globale Variablen
        self.serialWorker = None
        self.midiPort = None
        self.midi = None

        self.setWindowTitle("Serial To Midi")
        self.setMinimumWidth(500)

        self.layout = QVBoxLayout()

        # Info Lable
        self.infoLabel = QLabel("Select Com Port")
        self.layout.addWidget(self.infoLabel)

        # Com Port Selection
        self.setComPort = QComboBox()
        self.setComPort.addItems(serial_ports())
        self.setComPort.currentTextChanged.connect(self.setMidiPortSelection)
        self.layout.addWidget(self.setComPort)

        # Midi Info
        self.midiInfo = QLabel("Select Midi Port")
        self.layout.addWidget(self.midiInfo)

        # Midi Port Selection
        self.setMidiPort = QComboBox()
        self.setMidiPort.addItems(midi.getOpenMidiPort())
        self.setMidiPort.currentTextChanged.connect(self.midiPortChanged)
        self.layout.addWidget(self.setMidiPort)

        # Start Button
        self.startButton = QPushButton("Start Encoding")
        self.startButton.clicked.connect(self.startButtonPressed)
        self.layout.addWidget(self.startButton)

        # Stop Button
        self.stopButton = QPushButton("Stop Encoding")
        self.stopButton.clicked.connect(self.stopButtonPress)
        self.layout.addWidget(self.stopButton)

        # Input Debug Lable
        self.dataFromFader = QLabel("Input")
        self.layout.addWidget(self.dataFromFader)

        # ----- Fader ----------
        # creates 8 Labels horizontally
        self.faderList = [Fader] * 12

        self.layout2 = QHBoxLayout()

        for x in range(12):
            self.faderList[x] = Fader(x, self.layout2,self)

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

    # --------------- multi threading -----------------
    # Starts the Serial Connection
    def startButtonPressed(self):
        # If this returns False the Serial Port is not found
        usedSetup = serialInput.setup(self.comPort)

        if usedSetup is False:
            return

        if self.midiPort is None:
            print("No Midi port defined")
            return

        print("Starting Midi")
        self.midi = Midi(self.midiPort)

        self.serialWorker = Worker(usedSetup, self.midi, self.faderList)
        self.serialWorker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(self.serialWorker)

    # Stopps the running Serial Connection
    def stopButtonPress(self):
        if self.serialWorker:
            self.serialWorker.kill()
        else:
            print("No thread started")

    # Verbindung zu Signals für das GUI
    def progress_fn(self, split):
        for x in range(12):
            self.faderList[x].updateData(round(int(split[x]), -1))  # runden auf nächsten 10

    # ------------- Others -----------------------

    def setMidiPortSelection(self, s):
        print(s)
        self.comPort = s

    def midiPortChanged(self, s):
        self.midiPort = s

    def closeEvent(self, event):
        self.stopButtonPress()
        print("close")


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
