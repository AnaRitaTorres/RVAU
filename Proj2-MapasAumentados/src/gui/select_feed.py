from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from gui.gui_augment import MainWindow
from core.database import *

dialogs = []

class SelectFeed(QWidget):
    def __init__(self, item, test):
        super(SelectFeed, self).__init__()

        self.test = test

        self.item = item
        font = QtGui.QFont("Calibri", 15, QtGui.QFont.Bold)

        image = QPushButton("IMAGE")
        image.clicked.connect(self.init_image)
        image.setFont(font)
        image.setStyleSheet("QPushButton { height: 60px; padding: 30px; }")

        video = QPushButton("VIDEO")
        video.clicked.connect(self.init_video)
        video.setFont(font)
        video.setStyleSheet("QPushButton { height: 60px; padding: 30px; }")

        hbox = QHBoxLayout()
        hbox.addWidget(image)
        hbox.addWidget(video)
        self.setLayout(hbox)

    def init_image(self):
        maps = load_database()
        map_entry = get_map(self.item, maps)
        window = MainWindow('image', map_entry, self.test)
        dialogs.append(window)
        window.show()
        self.close()

    def init_video(self):
        maps = load_database()
        map_entry = get_map(self.item, maps)
        window = MainWindow('video', map_entry, self.test)
        dialogs.append(window)
        window.show()
        self.close()
