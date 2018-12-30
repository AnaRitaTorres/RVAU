from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QInputDialog
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QGuiApplication
from gui.graphic_scene import EditorScene
from gui.add_point import AddPoint
from core.database import *
from core.detector import *

# Color of point of interest on map
color_poi = (0, 0, 255)


# Window showing loaded image. Allows to see feature points and add points of interest
class DatabaseWindow(QMainWindow):
    # Signal main window that window was closed
    closed_window = QtCore.pyqtSignal()

    def __init__(self, test):
        QMainWindow.__init__(self)

        # Additional images
        self.image_filenames = []

        # Test mode active
        self.test = test

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

        self.dialogs = []
        self.saving = False
        self.show()

    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Database')

        # Resizes window
        screen_size = QtGui.QGuiApplication.primaryScreen().availableSize()
        self.resize(int(screen_size.width() * 4 / 5), int(screen_size.height() * 4 / 5))

        # Shows status bar message
        self.statusBar().showMessage('Load an image')

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
        self.load_action = self.toolbar_button('Load Image', 'Load an image', 'Ctrl+I')
        self.load_action.setCheckable(True)
        self.load_action.toggled.connect(self.open_image)
        self.toolbar.addAction(self.load_action)

        # Show or Hide Features Option
        self.features_action = self.toolbar_button('Show Keypoints', 'Shows feature points', 'Ctrl+F')
        self.features_action.setCheckable(True)
        self.features_action.setDisabled(True)
        self.features_action.toggled.connect(self.select_features)
        self.toolbar.addAction(self.features_action)

        # Add Points of Interest Option
        self.add_point_action = self.toolbar_button('Point of Interest', 'Add Point of Interest', 'Ctrl+P')
        self.add_point_action.setDisabled(True)
        self.add_point_action.triggered.connect(self.add_point)
        self.toolbar.addAction(self.add_point_action)

        # More images Option
        self.more_action = self.toolbar_button('More Images', 'Add More Images of Map', 'Ctrl+M')
        self.more_action.setDisabled(True)
        self.more_action.triggered.connect(self.more_images)
        self.toolbar.addAction(self.more_action)

        # Save and Quit Option
        self.save_action = self.toolbar_button('Save and Quit', 'Saves Points of Interest and Quits Application', 'Ctrl+S')
        self.save_action.setDisabled(True)
        self.save_action.triggered.connect(self.save_and_quit)
        self.toolbar.addAction(self.save_action)

    def open_image(self):
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Image', os.environ.get('HOME'),
                                                             'Images (*.png *.jpg)')
        if filename:
            self.load_image(filename)

            self.features_action.setDisabled(False)
            self.add_point_action.setDisabled(False)
            self.more_action.setDisabled(False)
            self.save_action.setDisabled(False)
            self.load_action.setDisabled(True)

    def load_image(self, filename):
        # Read original image
        img = cv2.imread(filename)

        # Run SIFT on map image
        results = runSIFT(filename, self.test)

        self.map_name = filename
        self.image = img
        self.features = results['img_features']
        self.features_info = results['pts_features']

        # Display loaded image
        self.editor_scene.display_image(self.image)

        # Show message after loading image
        self.statusBar().showMessage('Loaded image successfully!')

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

    # Triggered if More Images option is selected on toolbar
    def more_images(self):
        self.statusBar().showMessage('Adding map image...')
        filename, __ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Image', os.environ.get('HOME'),
                                                             'Images (*.png *.jpg)')
        if filename:
            self.image_filenames.append(filename)

            # Show message after loading image
            self.statusBar().showMessage('Added image successfully!')
        else:
            # Show message if user canceled
            self.statusBar().showMessage('Canceled adding map image')

    # Triggered if Save and Quit option is selected on toolbar
    def save_and_quit(self):
        # Saves Points of Interest in file
        self.statusBar().showMessage('Saving entry to database...')

        if len(self.pois) > 0:
            self.get_user_inputs()
        else:
            # Show error if no points of interest were added
            info_box = QtWidgets.QMessageBox(self)
            info_box.setWindowTitle("Error")
            info_box.setIcon(QtWidgets.QMessageBox.Critical)
            info_box.setText("No points of interest added!")
            return info_box.exec()

    # Get user inputs
    def get_user_inputs(self):
        # Creates a dialog for the new point of interest
        entry_name, ok_name = QInputDialog.getText(self, 'Saving Entry...', 'Enter map name:')

        if ok_name:
            # Checks if name entry is valid
            if entry_name == "":
                # Show error if no points of interest were added
                info_box = QtWidgets.QMessageBox(self)
                info_box.setWindowTitle("Error")
                info_box.setIcon(QtWidgets.QMessageBox.Critical)
                info_box.setText("Name invalid!")
                self.statusBar().showMessage('Error saving entry')
                return info_box.exec()

            map_scale, ok_scale = QInputDialog.getText(self, 'Saving Entry...', 'How many meters shown per 1cm? (int)')

            if ok_scale:
                if not map_scale.isnumeric():
                    # Show error if no points of interest were added
                    info_box = QtWidgets.QMessageBox(self)
                    info_box.setWindowTitle("Error")
                    info_box.setIcon(QtWidgets.QMessageBox.Critical)
                    info_box.setText("Invalid scale!")
                    self.statusBar().showMessage('Error saving entry')
                    return info_box.exec()

                print(entry_name, map_scale)
                self.statusBar().showMessage('Saving entry to database')
                save_database(entry_name, map_scale, self.map_name, self.image_filenames, self.features_info, self.pois, self.test)

                # Quits Application
                self.statusBar().showMessage('Quitting Application...')

                self.saving = True
                self.closed_window.emit()
                self.close()
            else:
                self.statusBar().showMessage('Canceled saving entry')
        else:
            self.statusBar().showMessage('Canceled saving entry')

    # Called when user tries to add point of interest. Gives clicked position
    def on_point_added(self, scene_position: QPointF):
        # Creates a dialog for the new point of interest
        dialog = AddPoint(scene_position, self.test)

        dialog.save_point.connect(self.on_point_saved)
        dialog.closed_window.connect(self.on_window_closed)

        dialog.exec_()

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
        if not self.saving:
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
