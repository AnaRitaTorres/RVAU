from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QImage
from PyQt5.Qt import Qt
from core.video import *
from core.matcher import *
from core.database import *
import time

from cv2 import *


# Window showing loaded image. Allows to see feature points and add points of interest
class MainWindow(QMainWindow):
    def __init__(self, mode, original_map, test):
        QMainWindow.__init__(self)

        # Test mode active
        self.test = test

        # Get base image
        self.original_image = get_base_image(original_map)

        # Check mode
        self.mode = mode

        # Configure window title, dimension, etc.
        self.configure_window()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.show()

        if self.mode == 'video':
            # self.statusBar().showMessage('Loading Webcam Feed...')
            QTimer.singleShot(1, self.startVideo)

        # Add toolbar
        self.toolbar = self.addToolBar('Main Toolbar')
        self.toolbar.setMovable(False)
        self.configure_toolbar()

    def startVideo(self):
        cap = VideoCapture(0)
        self.img = captureVideo(cap, self.original_image, self.test)
        self.display_image(self.img)
        while True:
            self.update()
            QApplication.processEvents()
            self.img = captureVideo(cap, self.original_image, self.test)
            self.update_image(self.img)
            time.sleep(0.1)
        cap.release()

    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Display')

        # Resizes window
        screen_size = QtGui.QGuiApplication.primaryScreen().availableSize()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setFixedSize(self.size())

        # Shows status bar message
        # self.statusBar().showMessage('Ready')

    def toolbar_button(self, text: str, tooltip: str = None, shortcut: str = None) -> QtWidgets.QAction:
        # Creates action
        action = QtWidgets.QAction(text, self)
        tooltip = tooltip if tooltip is not None else text

        if shortcut is not None:
            # Set shortcut
            action.setShortcut(shortcut)
            # Adds shortcut to tooltip
            tooltip += "<br><b>%s</b>" % action.shortcut().toString()

        # Set tooltip
        action.setToolTip(tooltip)
        return action

    def configure_toolbar(self):
        if self.mode == 'image':
            # Load Image Option
            self.open_action = self.toolbar_button('Load Image', 'Quits Application', 'Ctrl+I')
            self.open_action.triggered.connect(self.open_image)
            self.toolbar.addAction(self.open_action)

        # Quit Option
        quit_app = self.toolbar_button('Quit', 'Quits Application', 'Ctrl+S')
        quit_app.triggered.connect(self.quit_application)
        self.toolbar.addAction(quit_app)

    # Triggered when Load Image option on the toolbar is selected
    def open_image(self):
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Image', os.environ.get('HOME'),
                                                             'Images (*.png *.jpg)')
        if filename:
            # Read loaded image and display it
            img = cv2.imread(filename)
            arr = matchFeatures(img, self.original_image, self.test)
            if arr['img'] is not None:
                img = arr['img']
            img = draw_poi(img)
            if arr['angle'] is not None:
                img = draw_compass(img, arr['angle'])

            self.display_image(img)
            if arr['matrix'] is not None:
                print("HERE")
                # TODO: Fazer aqui pontos de interesse
            self.editor_scene.display_image(img)
            self.open_action.setDisabled(True)

    def quit_application(self):
        # self.statusBar().showMessage('Quitting Application...')
        self.close()

    def display_image(self, img):
        # Get QImage Format depending on number of dimensions
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        # Image attributes: height, width, channels (dimensions)
        h, w, d = img.shape

        # Create QImage with image information given by OpenCV
        q_image = QtGui.QImage(img, w, h, w * d, qformat)

        # Swap colors
        q_image = q_image.rgbSwapped()

        # Get pixmap
        pixmap = QtGui.QPixmap(q_image)
        self.show_points(pixmap)

    def update_image(self, img):
        # Get QImage Format depending on number of dimensions
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        # Image attributes: height, width, channels (dimensions)
        h, w, d = img.shape

        # Create QImage with image information given by OpenCV
        q_image = QtGui.QImage(img, w, h, w * d, qformat)

        # Swap colors
        q_image = q_image.rgbSwapped()

        # Get pixmap
        pixmap = QtGui.QPixmap(q_image)
        self.main_image.setPixmap(pixmap.scaled(self.width(), self.height() - 50, Qt.KeepAspectRatio))

    def show_points(self, pixmap):
        widget = QWidget()
        self.setCentralWidget(widget)

        # Show main image while keeping aspect ratio
        self.main_image = QLabel()
        self.main_image.setPixmap(pixmap.scaled(self.width(), self.height()-50, Qt.KeepAspectRatio))

        # Set up main layout (show main image
        main_layout = QHBoxLayout(widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_image)

        # Set up slideshow layout
        self.slideshow = QLabel(widget)
        self.slideshow.setStyleSheet("QLabel { background-color: #ffffff }")
        self.slideshow.setFixedSize(400, 375)

        # Set up point of interest's information (name, distance and image)
        self.name = QLabel("Name: University of london")
        self.distance = QLabel("Distance: 150m")

        self.image_poi = QLabel()
        point_of_interest = self.original_image.points[0].images[0]
        print(point_of_interest)
        pixmap = QtGui.QPixmap(point_of_interest)
        self.image_poi.setPixmap(pixmap.scaled(380, 300, Qt.KeepAspectRatio))

        # Set up previous and next buttons
        self.prev = QPushButton("Previous")
        self.next = QPushButton("Next")

        # Show buttons in horizontal layout
        prev_next = QHBoxLayout()
        prev_next.addWidget(self.prev)
        prev_next.addWidget(self.next)

        # Show all info in vertical layout
        self.slideshow_layout = QVBoxLayout()
        self.slideshow_layout.addWidget(self.name)
        self.slideshow_layout.addWidget(self.distance)
        self.slideshow_layout.addWidget(self.image_poi)
        self.slideshow_layout.addLayout(prev_next)

        self.slideshow.setLayout(self.slideshow_layout)

        # Move widget to top corner of the screen
        slideshow_position = self.geometry().topRight() - self.slideshow.geometry().topRight()
        self.slideshow.move(slideshow_position)

        self.update()
        QApplication.processEvents()

    # Triggered when window is closed
    def closeEvent(self, event):
        # Quit application
        quit()
