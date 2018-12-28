
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton


class PointOfInterest(QMainWindow):
    def __init__(self, position):
        QMainWindow.__init__(self)
        print(position)

        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.setText('Name:')
        self.lbl.adjustSize()

        qle = QLineEdit(self)
        self.lbl.move(17.5, 17.5)
        qle.resize(172.5, 30)
        qle.move(90, 10)

        button = QPushButton('ADD POINT', self)
        button.resize(250, 30)
        button.move(15, 50)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Point of Interest')
        self.show()
