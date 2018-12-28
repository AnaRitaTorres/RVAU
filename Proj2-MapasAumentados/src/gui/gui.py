from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QGuiApplication
from gui.graphic_scene import EditorScene
from gui.add_point import PointOfInterest
from core.utils import *

# Window showing loaded image. Allows to see feature points and add points of interest
class MainWindow(QMainWindow):
    def __init__(self, original_image, features, test, map_name):
        QMainWindow.__init__(self)

        # Test mode active
        self.test = test

        # Original map's name
        self.map_name = map_name

        # Original Image
        self.image = original_image

        # Image with feature points
        self.features = features

        # Strings relating to POIs
        self.pois = []

        # Configure window title, dimension, etc.
        self.configure_window()

        # Add and configure toolbar
        self.toolbar = self.addToolBar('Main Toolbar')
        self.configure_toolbar()

        # Canvas scene
        self.editor_scene = EditorScene()
        # Slot called when user tries to add Point of Interest
        self.editor_scene.add_point.connect(self.on_point_added)
        # Canvas view
        self.editor_view = QtWidgets.QGraphicsView(self.editor_scene)

        # Set image canvas as the central widget
        self.setCentralWidget(self.editor_view)

        # Display loaded image
        self.editor_scene.display_image(self.image)

        # The user may open more than one dialog to add points of interest
        self.dialogs = list()
        self.show()

    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Database')

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
        # Show or Hide Features Option
        features = self.toolbar_button('Show Keypoints', 'Shows feature points', 'Ctrl+F')
        features.setCheckable(True)
        features.toggled.connect(self.select_features)
        self.toolbar.addAction(features)

        # Add Points of Interest Option
        point_of_interest = self.toolbar_button('Point of Interest', 'Add Point of Interest', 'Ctrl+P')
        point_of_interest.triggered.connect(self.add_point)
        self.toolbar.addAction(point_of_interest)

        # Save and Quit Option
        save_and_quit = self.toolbar_button('Save and Quit', 'Saves Points of Interest and Quits Application', 'Ctrl+S')
        save_and_quit.triggered.connect(self.saveandquit)
        self.toolbar.addAction(save_and_quit)

        # Quit Option
        quit_act = self.toolbar_button('Quit', 'Quit application', 'Ctrl+Q')
        quit_act.triggered.connect(QtWidgets.QApplication.quit)
        self.toolbar.addAction(quit_act)

    # Triggered if Save and Quit option is selected on toolbar
    def saveandquit(self):
        # Saves Points of Interest in file
        self.statusBar().showMessage('Saving points of interest...')
        setupPOI(self.map_name + '_poi', self.test)
        savePOIs(self.map_name + '_poi', self.pois, self.test)

        # Quits Application
        self.statusBar().showMessage('Quitting Application...')
        quit()


    # Triggered if features options is selected on toolbar
    def select_features(self, toggled: bool):
        # If features option is toggled
        if toggled:
            # Show features
            self.editor_scene.display_image(self.features)
            self.statusBar().showMessage('Showing Features')

        # If features option is not togged
        else:
            # Show original image
            self.editor_scene.display_image(self.image)
            self.statusBar().showMessage('Hiding Features')

    # Triggered if option to add points of interest is clicked
    def add_point(self):
        self.statusBar().showMessage('Adding Point of Interest...')

        # Changes cursor to Cross Cursor
        QGuiApplication.setOverrideCursor(Qt.CrossCursor)

        # Canvas is now clickable
        self.editor_scene.clickable = True

    # Called when user tries to add point of interest. Gives clicked position
    def on_point_added(self, scene_position: QPointF):
        # Creates a dialog for the new point of interest
        dialog = PointOfInterest(scene_position, self.test)
        dialog.closed_window.connect(self.on_window_closed)
        self.dialogs.append(dialog)
        dialog.show()

    def on_window_closed(self, scene_position: QPointF):
        if self.test:
            print("\n Formatted Line: " + scene_position)
        self.pois.append(scene_position)
        self.statusBar().showMessage('Added Point of Interest')
