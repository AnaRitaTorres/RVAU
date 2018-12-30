from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from gui.gui_augment import MainWindow
from core.database import *

dialogs = []


# Allows to select between image and video feed
class SelectFeed(QWidget):
    closed_window = QtCore.pyqtSignal()

    def __init__(self, maps, item, test):
        super(SelectFeed, self).__init__()

        self.test = test

        self.maps = maps
        self.item = item

        self.init_widgets()

    # Sets up application layout
    def init_widgets(self):
        font = QtGui.QFont("Calibri", 15, QtGui.QFont.Bold)

        # Image button
        image_btn = QPushButton("IMAGE")
        image_btn.clicked.connect(self.init_image)
        image_btn.setFont(font)
        image_btn.setStyleSheet("QPushButton { height: 60px; padding: 30px; }")

        # Video button
        video_btn = QPushButton("VIDEO")
        video_btn.clicked.connect(self.init_video)
        video_btn.setFont(font)
        video_btn.setStyleSheet("QPushButton { height: 60px; padding: 30px; }")

        # Set up main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(image_btn)
        main_layout.addWidget(video_btn)
        self.setLayout(main_layout)

    # Triggered when image button is clicked
    def init_image(self):
        map_entry = get_map(self.item, self.maps)
        window = MainWindow('image', map_entry, self.test)
        dialogs.append(window)
        window.show()
        self.closed_window.emit()
        self.close()

    # Triggered when video button is clicked
    def init_video(self):
        map_entry = get_map(self.item, self.maps)
        window = MainWindow('video', map_entry, self.test)
        dialogs.append(window)
        window.show()
        self.closed_window.emit()
        self.close()
