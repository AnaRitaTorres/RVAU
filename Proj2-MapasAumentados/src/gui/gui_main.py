from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QApplication, QPushButton, QListWidgetItem

from gui.select_feed import SelectFeed
from gui.gui_database import *

dialogs = []


class MainWindow(QMainWindow):

    def __init__(self, maps, test):
        super().__init__()

        # Test mode
        self.test = test

        # Maps loaded from database
        self.maps = maps

        self.init_widgets()
        self.configure_window()

        self.show()

    # Shows widgets on the main layout
    def init_widgets(self):
        self.init_buttons()
        self.init_list()

        # Set up main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.list_box)
        self.main_layout.addSpacing(15)
        self.main_layout.addLayout(self.btn_box)

        # Set main layout as central widget
        window = QWidget()
        window.setLayout(self.main_layout)
        self.setCentralWidget(window)

    # Fill list and add it to vertical layout (list_box)
    def init_list(self):
        # Map list widget
        self.list_maps = QListWidget()

        # Fill map list
        self.fill_list()

        # Set up list label
        maps_label = QLabel("List of maps on database:")
        font = QtGui.QFont("Calibri", 15, QtGui.QFont.Bold)
        maps_label.setFont(font)

        # Add widgets to list vertical layout
        self.list_box = QVBoxLayout()
        self.list_box.addWidget(maps_label)
        self.list_box.addWidget(self.list_maps)

    def fill_list(self):
        if len(self.maps) == 0:
            # If maps list is empty, add empty element and disable list
            item = QListWidgetItem()
            item.setText("No map entries on the database yet.")
            self.list_maps.addItem(item)
            self.list_maps.setDisabled(True)
        else:
            # If maps list is not empty, fill it with map entries and enable it
            self.list_maps.setDisabled(False)

            # Fill maps list
            map_names = get_map_names(self.maps)

            # Fill map entries
            for map_entry in map_names:
                self.list_maps.addItem(map_entry)

    # Init buttons and add them to vertical layout (btn_box)
    def init_buttons(self):
        self.btn_box = QVBoxLayout()

        # Add buttons to manage map list
        add_button = QPushButton("Add Entry")
        add_button.clicked.connect(self.add_entry)

        select_button = QPushButton("Select Entry")
        select_button.clicked.connect(self.select_entry)

        remove_button = QPushButton("Remove Entry")

        # Set buttons style (height and padding)
        add_button.setStyleSheet("QPushButton { height: 50px; padding: 10px; }")
        select_button.setStyleSheet("QPushButton { height: 50px; padding: 10px; }")
        remove_button.setStyleSheet("QPushButton { height: 60px; padding: 10px; }")

        # Set buttons font
        font = QtGui.QFont("Calibri", 15, QtGui.QFont.Bold)
        add_button.setFont(font)
        select_button.setFont(font)
        remove_button.setFont(font)

        # Add widgets to buttons vertical layout
        self.btn_box.setSpacing(10)
        self.btn_box.addWidget(add_button)
        self.btn_box.addWidget(select_button)
        self.btn_box.addWidget(remove_button)
        self.btn_box.addStretch(1)

    # Set up main window
    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Maps')

        # Resizes window
        screen_size = QtGui.QGuiApplication.primaryScreen().availableSize()
        self.resize(int(screen_size.width() * 4 / 5), int(screen_size.height() * 4 / 5))

    # Triggered when add entry button is clicked
    def add_entry(self):
        # Init database window
        window = DatabaseWindow(self.test)
        # Signal when window is closed to update list
        window.closed_window.connect(self.on_database_closed)
        dialogs.append(window)
        window.show()

    # Triggered when an item is selected
    def select_entry(self):
        row = self.list_maps.currentRow()
        item = self.list_maps.item(row)

        if item is not None:
            print(item.text())

            # Shows new window to select between video and image
            dialog = SelectFeed(item.text(), self.test)
            self.setCentralWidget(dialog)

    # Triggered when database window is closed
    def on_database_closed(self):
        # Update map entries
        self.maps = load_database()

        # Clear list
        self.list_maps.clear()

        # Update list items
        self.fill_list()
        self.update()
        QApplication.processEvents()
