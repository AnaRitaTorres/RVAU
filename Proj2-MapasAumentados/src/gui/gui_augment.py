from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, QPointF, QThread, QTimer
from PyQt5.QtGui import QGuiApplication
from gui.graphic_scene import EditorScene
from core.video import *
import time
from cv2 import *

# Window showing loaded image. Allows to see feature points and add points of interest
class MainWindow(QMainWindow):
    def __init__(self, mode, original_image, test):
        QMainWindow.__init__(self)

        # Test mode active
        self.test = test

        # Check mode
        if mode == 'image':
            # Original Image
            self.image = original_image
            self.mode = mode
        elif mode == 'video':
            self.image = None
            self.mode = mode
        else:
            print('Incorrect mode detected! Quitting...')
            quit()

        # Configure window title, dimension, etc.
        self.configure_window()

        # Add and configure toolbar
        self.toolbar = self.addToolBar('Main Toolbar')
        self.configure_toolbar()

        # Canvas scene
        self.editor_scene = EditorScene()
        # Canvas view
        self.editor_view = QtWidgets.QGraphicsView(self.editor_scene)

        # Set image canvas as the central widget
        self.setCentralWidget(self.editor_view)

        # The user may open more than one dialog to add points of interest
        self.dialogs = list()
        self.show()
        
        # Display loaded image
        if (self.mode == 'image'):
            self.editor_scene.display_image(self.image)
        elif (self.mode == 'video'):
            self.statusBar().showMessage('Loading Webcam Feed...')
            QTimer.singleShot(1, self.startVideo)
                
    def startVideo(self):
        cap = VideoCapture(0)
        while True:
            self.update()
            QApplication.processEvents()
            self.img = captureVideo(cap)
            self.editor_scene.display_image(self.img)
        cap.release()

    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Display')

        # Resizes window
        screen_size = QtGui.QGuiApplication.primaryScreen().availableSize()
        self.resize(int(screen_size.width() * 4 / 5), int(screen_size.height() * 4 / 5))

        # Shows status bar message
        self.statusBar().showMessage('Ready')

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
        quit_app = self.toolbar_button('Quit', 'Quits Application', 'Ctrl+S')
        quit_app.triggered.connect(self.quit_application)
        self.toolbar.addAction(quit_app)

    def quit_application(self):
        self.statusBar().showMessage('Quitting Application...')
        quit()
