from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication, QImage


# Subclass of QGraphicsScene, handles image loading on canvas and mouse events
class EditorScene(QtWidgets.QGraphicsScene):
    add_point = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()

        # Boolean variable initially set to False, user can't add Points of Interest until he says he wants to
        self.clickable = False

    # Displays Image on canvas
    def display_image(self, img):
        # Clear canvas
        self.clear()

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

        # Show image
        self.addPixmap(QtGui.QPixmap(q_image))

    # Overrides mouse press event to get position on map
    def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        # If user clicked on the left button, nothing happens
        if event.button() != Qt.LeftButton:
            return

        # If map is clickable, get position
        if self.clickable:
            # Map position in which user clicked
            position = event.scenePos()

            # Change cursor to default
            QGuiApplication.setOverrideCursor(Qt.ArrowCursor)

            # Map stops being clickable
            self.clickable = False

            self.add_point.emit(position)

