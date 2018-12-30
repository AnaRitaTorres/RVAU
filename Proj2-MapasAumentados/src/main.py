# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program acts as the preparation for the map
# It can be run on a normal or test mode

from PyQt5.QtWidgets import QApplication
import sys
import argparse
from gui.gui_main import MainWindow
from core.database import *


if __name__ == '__main__':
    # Load up parameters
    # python main.py [-t | --test]
    parser = argparse.ArgumentParser(description="Sets up a map and its points of interest")
    parser.add_argument('-t', '--test', dest='test', action='store_true')

    maps = load_database()

    arguments = parser.parse_args()

    # if test flag detected
    if arguments.test:
        print('Starting in Test Mode!')

    app = QApplication(sys.argv)
    window = MainWindow(maps, arguments.test)
    sys.exit(app.exec_())
