from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, QPoint
from PyQt5.QtGui import QImage
from PyQt5.Qt import Qt
from core.video import *
from core.matcher import *
from core.database import *
import time
import cv2

poi_image_size = (380, 280)


# Window showing loaded image. Allows to see feature points and add points of interest
class MainWindow(QMainWindow):
    def __init__(self, mode, original_map, props, test):
        QMainWindow.__init__(self)

        # Test mode active
        self.test = test

        # Get base image
        self.original_image = get_base_image(original_map)

        # Get map scale
        self.scale = original_map.scale

        # Check mode
        self.mode = mode

        self.props = props

        # Configure window title, dimension, etc.
        self.configure_window()

        # Image index for points of interest
        self.index = 0

        # Point of interest
        self.point_of_interest = None

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.show()

        if self.mode == 'video':
            if self.test:
                print('Loading Webcam Feed...')
            QTimer.singleShot(1, self.startVideo)

        # Add toolbar
        self.toolbar = self.addToolBar('Main Toolbar')
        self.toolbar.setMovable(False)
        self.configure_toolbar()

    def startVideo(self):
        cap = VideoCapture(0)
        results = captureVideo(cap, self.mode, self.original_image, self.scale, self.test)

        self.display_image(results['img'], results['point'], results['distance'])

        while True:
            self.update()
            QApplication.processEvents()
            results = captureVideo(cap, self.mode, self.original_image, self.scale, self.test)
            self.update_image(results['img'], results['point'], results['distance'])
            time.sleep(0.1)
        cap.release()

    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Augment map')

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
        if self.mode == 'image':
            # Load Image Option
            self.open_action = self.toolbar_button('Load Image', 'Quits Application', 'Ctrl+I')
            self.open_action.triggered.connect(self.open_image)
            self.toolbar.addAction(self.open_action)

            if self.test:
                print('Waiting for user to upload a map image to augment...')

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

            if self.test:
                print('Matching features between original image of the map and current image')

            arr = matchFeatures(self.mode, img, self.original_image, self.test)

            point_of_interest = None
            distance = 0

            if arr['img'] is not None:
                if self.test:
                    print('Drawing center of image')
                img = arr['img']
            if arr['angle'] is not None:
                if self.test:
                    print('Drawing compass on image')
                img = draw_compass(img, arr['angle'])
            if arr['matrix'] is not None:
                if self.test:
                    print('Drawing points of interest')
                p_arr = get_pois(self.original_image.points, arr['matrix'])
                results = draw_poi(img, p_arr, self.scale)

                img = results['img']
                point_of_interest = results['point']
                distance = results['distance']

            if self.point_of_interest is None:
                self.display_image(img, point_of_interest, distance)
            else:
                self.update_image(img, point_of_interest, distance)
            # self.open_action.setDisabled(True)

            if self.test:
                print('Loaded map image successfully!')

    # Triggered when Quit option on the toolbar is selected
    def quit_application(self):
        self.close()

    # Display image and closest point of interest for the first time
    def display_image(self, img, point_of_interest, distance):
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

        # Set up UI for image and closest point of interest
        self.show_point(pixmap, point_of_interest, distance)

    # Update image and closest point of interest
    def update_image(self, img, point_of_interest, distance):
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

        # Checks if current point of interest is None
        if point_of_interest is None:
            # Hide slideshow if true
            self.slideshow.hide()

            if self.mode == 'image':
                # Show error if no points of interest were added
                info_box = QtWidgets.QMessageBox(self)
                info_box.setWindowTitle("Point of Interest")
                info_box.setIcon(QtWidgets.QMessageBox.Warning)
                info_box.setText("No point of interest found!")
                return info_box.exec()
        else:
            # Show slideshow if not
            self.slideshow.show()

            # Set images array for point of interest
            self.images_poi = point_of_interest.images

            # Update distance to point of interest
            dist = '<b>Distance:</b> {} m'.format(distance)
            self.distance.setText(dist)

            # Checks if previous point of interest is None
            if self.point_of_interest is None:
                self.update_poi(point_of_interest)
            else:
                # Checks if previous point of interest is equal to current point of interest
                if self.point_of_interest.name != point_of_interest.name:
                    self.update_poi(point_of_interest)

    # Update point of interest information
    def update_poi(self, point_of_interest):
        # Update point of interest
        self.point_of_interest = point_of_interest

        # Update point of interest name
        name = '<b>Name:</b> {}'.format(point_of_interest.name)
        self.name.setText(name)

        # Update point of interest image
        self.index = 0
        image_point = point_of_interest.images[self.index]

        pixmap_poi = QtGui.QPixmap(image_point)
        self.image_poi.setPixmap(pixmap_poi.scaled(poi_image_size[0], poi_image_size[1], Qt.KeepAspectRatio))

        # Set previous and next buttons to disabled or not depending on number of images
        if len(self.images_poi) < 2:
            self.prev.setDisabled(True)
            self.next.setDisabled(True)
        else:
            self.prev.setDisabled(False)
            self.next.setDisabled(False)

    # Sets up UI for image and closest point of interest
    def show_point(self, image, point_of_interest, distance):
        self.point_of_interest = point_of_interest

        widget = QWidget()
        self.setCentralWidget(widget)

        # Show main image while keeping aspect ratio
        self.main_image = QLabel()
        self.main_image.setPixmap(image.scaled(self.width(), self.height()-50, Qt.KeepAspectRatio))

        # Set up main layout (show main image)
        main_layout = QHBoxLayout(widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.main_image)

        # Set up slideshow layout
        self.slideshow = QLabel(widget)
        self.slideshow.setStyleSheet("QLabel { background-color: #ffffff }")
        self.slideshow.setFixedSize(400, 375)

        # Check if point of interest exists
        if point_of_interest is not None:
            # If it exists, show correct name and distance
            name = '<b>Name:</b> {}'.format(point_of_interest.name)
            dist = '<b>Distance:</b> {} m'.format(distance)

            # Set images array for point of interest
            self.images_poi = point_of_interest.images
        else:
            name = ""
            dist = ""
            self.images_poi = []

        self.name = QLabel(name)
        self.distance = QLabel(dist)

        self.image_poi = QLabel()
        self.index = 0
        self.image_poi.setFixedSize(poi_image_size[0], poi_image_size[1])

        # Show point of interest images if it exists
        if self.point_of_interest is not None:
            image_point = point_of_interest.images[self.index]
            pixmap = QtGui.QPixmap(image_point)
            self.image_poi.setPixmap(pixmap.scaled(poi_image_size[0], poi_image_size[1], Qt.KeepAspectRatio))

        # Set up previous and next buttons
        self.prev = QPushButton("Previous")
        self.prev.clicked.connect(self.on_prev_clicked)
        self.next = QPushButton("Next")
        self.next.clicked.connect(self.on_next_clicked)

        if len(self.images_poi) < 2 or point_of_interest is None:
            self.prev.setDisabled(True)
            self.next.setDisabled(True)

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

        # If point of interest does not exist, hide slideshow
        if point_of_interest is None:
            self.slideshow.hide()

            if self.mode == 'image':
                # Show error if no points of interest were added
                info_box = QtWidgets.QMessageBox(self)
                info_box.setWindowTitle("Point of Interest")
                info_box.setIcon(QtWidgets.QMessageBox.Warning)
                info_box.setText("No point of interest found!")
                return info_box.exec()

        self.update()
        QApplication.processEvents()

    # Triggered when previous button is clicked
    def on_prev_clicked(self):
        last_index = len(self.point_of_interest.images) - 1

        if self.index > 0:
            self.index = self.index - 1
        else:
            self.index = last_index

        image_point = self.point_of_interest.images[self.index]
        pixmap_poi = QtGui.QPixmap(image_point)
        self.image_poi.setPixmap(pixmap_poi.scaled(poi_image_size[0], poi_image_size[1], Qt.KeepAspectRatio))

    # Triggered when next button is clicked
    def on_next_clicked(self):
        last_index = len(self.point_of_interest.images) - 1

        if self.index < last_index:
            self.index = self.index + 1
        else:
            self.index = 0

        image_point = self.point_of_interest.images[self.index]
        pixmap_poi = QtGui.QPixmap(image_point)
        self.image_poi.setPixmap(pixmap_poi.scaled(poi_image_size[0], poi_image_size[1], Qt.KeepAspectRatio))

    # Triggered when window is closed
    def closeEvent(self, event):
        # Quit application
        quit()
