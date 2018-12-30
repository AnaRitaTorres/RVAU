from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer
from gui.graphic_scene import EditorScene
from core.video import *
from core.matcher import *
from core.database import *

from cv2 import *


# Window showing loaded image. Allows to see feature points and add points of interest
class MainWindow(QMainWindow):
    def __init__(self, mode, original_map, test):
        QMainWindow.__init__(self)

        # Test mode active
        self.test = test

        # Get base image
        self.original_image = get_base_image(original_map)

        print(self.original_image.filename)

        # Check mode
        self.mode = mode

        # Configure window title, dimension, etc.
        self.configure_window()

        # Canvas scene
        self.editor_scene = EditorScene()
        # Canvas view
        self.editor_view = QtWidgets.QGraphicsView(self.editor_scene)

        # Set image canvas as the central widget
        self.setCentralWidget(self.editor_view)
        self.show()
        
        # Display loaded image
        if self.mode == 'image':
            # Add toolbar with option to load image
            self.toolbar = self.addToolBar('Main Toolbar')
            self.configure_toolbar()
        elif self.mode == 'video':
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
        # Load Image Option
        self.open_action = self.toolbar_button('Load Image', 'Quits Application', 'Ctrl+I')
        self.open_action.triggered.connect(self.open_image)
        self.toolbar.addAction(self.open_action)

    # Triggered when Load Image option on the toolbar is selected
    def open_image(self):
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Image', os.environ.get('HOME'),
                                                             'Images (*.png *.jpg)')
        if filename:
            # Read loaded image and display it
            img = cv2.imread(filename)
            img = draw_poi(img)
            self.editor_scene.display_image(img)
            self.open_action.setDisabled(True)

    # Triggered when window is closed
    def closeEvent(self, event):
        # Quit application
        quit()
