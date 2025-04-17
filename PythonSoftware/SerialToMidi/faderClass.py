from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QStyle

from PythonSoftware.SerialToMidi.faderSettingMenu import FaderMenu


class Fader:
    def __init__(self, name, placeIntoElement, mainWindow):
        layout = QVBoxLayout()

        self.mainWindow = mainWindow

        self.midiNote = 0
        self.midiVelocity = 0

        self._name = name

        self._nameLable = QLabel(str(self._name))
        self._nameLable.setStyleSheet("background-color: yellow;")
        layout.addWidget(self._nameLable)

        self.data = 0
        self._dataDisplay = QLabel(str(self.data))
        layout.addWidget(self._dataDisplay)

        self._button = QPushButton("S")
        self._button.clicked.connect(self.buttonClick)
        self._button.setStyleSheet("background-color: gray;")
        self._button.setMinimumWidth(30)
        self._button.setMinimumHeight(30)
        layout.addWidget(self._button)

        self._faderUi = QWidget()
        self._faderUi.setStyleSheet("border: 1px solid black;")
        self._faderUi.setLayout(layout)
        placeIntoElement.addWidget(self._faderUi)

    # updates label with new Data
    def updateData(self, data):
        self.data = data
        self._dataDisplay.setText(str(data))

    def buttonClick(self):
        self.w = FaderMenu(self._name, self.mainWindow)
        self.w.show()
