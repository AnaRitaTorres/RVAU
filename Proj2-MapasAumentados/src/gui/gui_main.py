from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QApplication, QPushButton, QListWidgetItem

from gui.select_feed import SelectFeed
from gui.gui_database import *

dialogs = []


class MainWindow(QMainWindow):

    def __init__(self, maps, test):
        super().__init__()

        self.test = test
        self.maps = maps
        self.list_maps = QListWidget()

        self.selected_item = None

        self.initial_widgets()
        self.configure_window()

        # Prevent dialogs from being garbage collected
        self.dialogs = []

        self.show()

    def initial_widgets(self):
        self.fill_list()
        self.init_buttons()

        hbox = QHBoxLayout()
        vbox_list = QVBoxLayout()
        maps_label = QLabel("List of maps on database:")
        font = QtGui.QFont("Calibri", 15, QtGui.QFont.Bold)
        maps_label.setFont(font)
        vbox_list.addWidget(maps_label)

        if len(self.maps) == 0:
            item = QListWidgetItem()
            item.setText("No map entries on the database yet.")
            self.list_maps.addItem(item)
            self.list_maps.setDisabled(True)

        vbox_list.addWidget(self.list_maps)
        hbox.addLayout(vbox_list)
        hbox.addSpacing(15)
        hbox.addLayout(self.vbox)

        window = QWidget()
        window.setLayout(hbox)
        self.setCentralWidget(window)

    def fill_list(self):
        # Fill maps list
        map_names = get_map_names(self.maps)

        for map_entry in map_names:
            self.list_maps.addItem(map_entry)

    def init_buttons(self):
        self.vbox = QVBoxLayout()

        # Add buttons
        add_button = QPushButton("Add Entry")
        add_button.clicked.connect(self.add_entry)

        select_button = QPushButton("Select Entry")
        select_button.clicked.connect(self.select_entry)

        remove_button = QPushButton("Remove Entry")

        add_button.setStyleSheet("QPushButton { height: 50px; padding: 10px; }")
        select_button.setStyleSheet("QPushButton { height: 50px; padding: 10px; }")
        remove_button.setStyleSheet("QPushButton { height: 60px; padding: 10px; }")

        font = QtGui.QFont("Calibri", 15, QtGui.QFont.Bold)
        add_button.setFont(font)
        select_button.setFont(font)
        remove_button.setFont(font)

        self.vbox.setSpacing(10)
        self.vbox.addWidget(add_button)
        self.vbox.addWidget(select_button)
        self.vbox.addWidget(remove_button)
        self.vbox.addStretch(1)

        return self.vbox

    def configure_window(self):
        # Sets window title
        self.setWindowTitle('Maps')

        # Resizes window
        screen_size = QtGui.QGuiApplication.primaryScreen().availableSize()
        self.resize(int(screen_size.width() * 4 / 5), int(screen_size.height() * 4 / 5))

    def add_entry(self):
        window = DatabaseWindow(self.test)
        window.closed_window.connect(self.on_database_closed)
        dialogs.append(window)
        window.show()

    def select_entry(self):
        row = self.list_maps.currentRow()
        self.selected_item = self.list_maps.item(row)

        if self.selected_item is not None:
            print(self.selected_item.text())
            dialog = SelectFeed(self.selected_item, self.test)
            self.setCentralWidget(dialog)

    def on_database_closed(self):
        self.list_maps.setDisabled(False)

        self.maps = load_database()
        self.list_maps.clear()

        self.fill_list()
        self.update()
        QApplication.processEvents()
