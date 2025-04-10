from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class Fader:
    def __init__(self,name,placeIntoElement):
        self._layout = QVBoxLayout()

        self._nameLable = QLabel(str(name))
        self._layout.addWidget(self._nameLable)

        self.data = 0
        self._dataDisplay = QLabel(str(self.data))
        self._layout.addWidget(self._dataDisplay)

        self._button = QPushButton()
        self._layout.addWidget(self._button)

        self._faderUi = QWidget()
        self._faderUi.setLayout(self._layout)
        placeIntoElement.addWidget(self._faderUi)

    # updates label with new Data
    def updateData(self,data):
        self.data = data
        self._dataDisplay.setText(str(data))



