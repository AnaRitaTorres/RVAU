from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QImage
from PyQt5.Qt import Qt
from core.video import *
from core.matcher import *
from core.database import *
from gui.graphic_scene import *
import time
import cv2
from gui.gui_augment import MainWindow
from core.calibration import *

dialogs = []

# Window showing loaded image. Allows to see feature points and add points of interest
class Calibration(QMainWindow):
    def __init__(self, mode, original_map, test):
        QMainWindow.__init__(self)

        # Test mode active
        self.test = test

        self.map_entry = original_map

        # Check mode
        self.mode = mode

        # Configure window title, dimension, etc.
        self.configure_window()

        self.init_buttons()

        self.editor_scene = EditorScene()
        self.editor_view = QtWidgets.QGraphicsView(self.editor_scene)
        self.setCentralWidget(self.editor_view)
        self.show()

        self.cap = VideoCapture(0)

        # Add toolbar
        self.toolbar = self.addToolBar('Main Toolbar')
        self.toolbar.setMovable(False)
        self.configure_toolbar()

        if self.mode == 'video':
            if self.test:
                print('Loading Webcam Feed...')
            QTimer.singleShot(1, self.startVideo)

    # Init buttons and add them to vertical layout (btn_box)
    def init_buttons(self):
        self.btn_box = QVBoxLayout()

        # Add buttons to manage map list
        add_button = QPushButton("TAKE CALIBRATION PICTURE")
        #add_button.clicked.connect(self.add_entry)

        # Set buttons style (height and padding)
        add_button.setStyleSheet("QPushButton { height: 50px; padding: 10px; }")

        # Set buttons font
        font = QtGui.QFont("Calibri", 15, QtGui.QFont.Bold)
        add_button.setFont(font)

        # Add widgets to buttons vertical layout
        self.btn_box.setSpacing(10)
        self.btn_box.addWidget(add_button)
        self.btn_box.addStretch(1)


    def startVideo(self):
        while True:

            self.update()
            QApplication.processEvents()
            
            if self.cap is None:
                break

            ret, frame = self.cap.read()

            # Resize image a bit
            height, width, depth = frame.shape
            new_height = 1.2 * height
            new_width = 1.2 * width
            new_frame = resize(frame, (int(new_width), int(new_height)))

            self.curr_frame = new_frame
            self.editor_scene.display_image(new_frame)

            time.sleep(0.1)

    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Augment map (Calibration)')
        
        # Set window as maximized
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowMaximized)

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

        # Quit Option
        calibrate_app = self.toolbar_button('Take Calibration Picture', 'Takes Picture to Calibrate Camera', 'Enter')
        calibrate_app.triggered.connect(self.take_calibrate)
        self.toolbar.addAction(calibrate_app)

        # Quit Option
        quit_app = self.toolbar_button('Quit', 'Quits Application', 'Ctrl+S')
        quit_app.triggered.connect(self.quit_application)
        self.toolbar.addAction(quit_app)

    def take_calibrate(self):

        ret, mtx, dist, rvecs, tvecs = do_calibration(self.curr_frame)

        if not ret:
            return

        self.cap.release()
        self.cap = None

        window = MainWindow('video', self.map_entry, {'ret': ret, 'mtx': mtx, 'dist': dist, 'rvecs': rvecs, 'tvecs': tvecs}, self.test)
        dialogs.append(window)
        window.show()
        #self.close()

    # Triggered when Quit option on the toolbar is selected
    def quit_application(self):
        self.close()

    # Triggered when window is closed
    def closeEvent(self, event):
        # Quit application
        quit()
