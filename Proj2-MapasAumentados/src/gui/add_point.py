from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QTextEdit, QWidget
from PyQt5.QtCore import Qt


class PointOfInterest(QMainWindow):
    def __init__(self, position):
        super().__init__()
        print(position)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        self.init_widgets(position)
        self.configure_window()

    def init_widgets(self, position):
        position_x = int(position.x())
        position_y = int(position.y())

        text_position = 'Point Position: (x: {:d}, y: {:d})'.format(position_x, position_y)
        position_label = QLabel(text_position)
        position_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(position_label)

        name_label = QLabel('Name')
        name_edit = QLineEdit()

        upload_btn = QPushButton('Upload Image', self)
        upload_label = QLabel('Uploaded Images: 0')

        grid = QGridLayout()
        grid.setSpacing(15)

        grid.addWidget(name_label, 1, 0)
        grid.addWidget(name_edit, 1, 1)

        grid.addWidget(upload_btn, 2, 0)
        grid.addWidget(upload_label, 2, 1)

        self.layout.addLayout(grid)

        confirm_btn = QPushButton('ADD POINT', self)

        self.layout.addWidget(confirm_btn)

        window = QWidget()
        window.setLayout(self.layout)
        self.setCentralWidget(window)

    def configure_window(self):
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Point of Interest')
        self.show()

