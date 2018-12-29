from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QGuiApplication
from gui.graphic_scene import EditorScene
from gui.add_point import AddPoint
from core.database import *

color_poi = (0, 0, 255)


# Window showing loaded image. Allows to see feature points and add points of interest
class MainWindow(QMainWindow):
    def __init__(self, original_image, features_image, features_info, test, map_name):
        QMainWindow.__init__(self)

        # Test mode active
        self.test = test

        # Original map's name
        self.map_name = map_name

        # Original Image
        self.image = original_image

        # Image with feature points
        self.features = features_image

        # Serialized features information
        self.features_info = features_info

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
        self.features_action = self.toolbar_button('Show Keypoints', 'Shows feature points', 'Ctrl+F')
        self.features_action.setCheckable(True)
        self.features_action.toggled.connect(self.select_features)
        self.toolbar.addAction(self.features_action)

        # Add Points of Interest Option
        point_of_interest = self.toolbar_button('Point of Interest', 'Add Point of Interest', 'Ctrl+P')
        point_of_interest.triggered.connect(self.add_point)
        self.toolbar.addAction(point_of_interest)

        # Save and Quit Option
        save_and_quit = self.toolbar_button('Save and Quit', 'Saves Points of Interest and Quits Application', 'Ctrl+S')
        save_and_quit.triggered.connect(self.save_and_quit)
        self.toolbar.addAction(save_and_quit)

    # Triggered if Save and Quit option is selected on toolbar
    def save_and_quit(self):
        # Saves Points of Interest in file
        self.statusBar().showMessage('Saving points of interest...')
        save_database(self.map_name, self.features_info, self.pois)

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
        dialog = AddPoint(scene_position, self.test)
        dialog.save_point.connect(self.on_point_saved)
        dialog.closed_window.connect(self.on_window_closed)
        self.dialogs.append(dialog)
        dialog.show()

    # Triggered when point of interest pop-up is closed without saving
    def on_window_closed(self):
        self.statusBar().showMessage('Canceled adding Point Of Interest')

    # Triggered when point of interest is saved
    def on_point_saved(self, point: PointOfInterest):
        self.pois.append(point)
        self.statusBar().showMessage('Added Point of Interest')

        # Draw a circle on point in which user added point of interest
        self.image = cv2.circle(self.image, (point.position_x, point.position_y), 20, color_poi, 2)
        self.features = cv2.circle(self.features, (point.position_x, point.position_y), 20, color_poi, 2)

        # See if features toggle is checked
        if self.features_action.isChecked():
            # Display features if it's checked
            self.editor_scene.display_image(self.features)
        else:
            # Display original image if it's not
            self.editor_scene.display_image(self.image)

    # Close event triggered when user tries to close main window
    def closeEvent(self, event):
        # Shows pop-up asking user whether he wants to close without saving
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "You haven't saved the map entry yet!<br>"
                                               "Are you sure you want to close?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        # Accept or ignore close event depending on user's response
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
