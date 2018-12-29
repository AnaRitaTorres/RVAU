from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QTextEdit, QWidget
from PyQt5.QtCore import Qt
from core.database import *


# Window triggered when user tries to add Point of Interest on map
class AddPoint(QMainWindow):
    # Signal main window that point is being saved
    save_point = QtCore.pyqtSignal(object)

    # Signal main window that window was closed
    closed_window = QtCore.pyqtSignal()

    def __init__(self, position, test):
        super().__init__()

        # Is in test mode
        self.test = test

        # Images uploaded by user
        self.images = []

        # Get X Position
        self.position_x = int(position.x())

        # Get Y Position
        self.position_y = int(position.y())

        # Main layout
        self.layout = QVBoxLayout()

        # Init window widgets
        self.init_widgets()

        # Configure window and show it
        self.configure_window()

    def init_widgets(self):
        # Show position label
        text_position = 'Point Position: (x: {:d}, y: {:d})'.format(self.position_x, self.position_y)
        position_label = QLabel(text_position)
        position_label.setAlignment(Qt.AlignCenter)

        # Name label
        name_label = QLabel('Name')
        # Name input
        self.name_edit = QLineEdit()

        # Button to upload image
        upload_btn = QPushButton('Upload Image', self)
        upload_btn.adjustSize()
        upload_btn.clicked.connect(self.add_image)

        # Label showing number of uploaded images
        upload_text = 'Uploaded Images: {:d}'.format(len(self.images))
        self.upload_label = QLabel(upload_text)

        # Grid Layout
        grid = QGridLayout()
        grid.setSpacing(15)

        # Point of Interest Name Row
        grid.addWidget(name_label, 1, 0)
        grid.addWidget(self.name_edit, 1, 1)

        # Upload Images Row
        grid.addWidget(upload_btn, 2, 0)
        grid.addWidget(self.upload_label, 2, 1)

        # Add Point Button
        self.confirm_btn = QPushButton('ADD POINT', self)
        self.confirm_btn.clicked.connect(self.add_point)

        # Set Main Layout Widgets
        self.layout.setSpacing(15)
        self.layout.addWidget(position_label)
        self.layout.addLayout(grid)
        self.layout.addWidget(self.confirm_btn)

        # Set Central Widget
        window = QWidget()
        window.setLayout(self.layout)
        self.setCentralWidget(window)

    # Triggered when user tries to add image to point of interest
    def add_image(self):
        # Opens dialog to add Images of type .png and .jpg
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Image', os.environ.get('HOME'),
                                                             'Images (*.png *.jpg)')
        # If filename is valid
        if filename:
            self.images.append(filename)

        # Update UI text showing number of images uploaded
        upload_text = 'Uploaded Images: {:d}'.format(len(self.images))
        self.upload_label.setText(upload_text)

    # Triggered when user tries to add point
    def add_point(self):
        # Check if name is valid
        if self.name_edit.text() == '':
            info_box = QtWidgets.QMessageBox(self)
            info_box.setWindowTitle("Error")
            info_box.setIcon(QtWidgets.QMessageBox.Critical)
            info_box.setText("Name can't be empty!")
            return info_box.exec()

        # Check if Point of Interest has images
        if len(self.images) == 0:
            info_box = QtWidgets.QMessageBox(self)
            info_box.setWindowTitle("Error")
            info_box.setIcon(QtWidgets.QMessageBox.Critical)
            info_box.setText("Need to add at least a image!")
            return info_box.exec()

        if self.test:
            print('Saving point (x: {:d}, y: {:d})'.format(self.position_x, self.position_y))

        # Signal main window that this window closed
        point = PointOfInterest(self.position_x, self.position_y, self.name_edit.text(), self.images)
        self.save_point.emit(point)
        return self.close()

    # Sets up window
    def configure_window(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Point of Interest')
        self.show()

    # Triggered when user tries to close this window
    def closeEvent(self, event):
        self.closed_window.emit()
        event.accept()
