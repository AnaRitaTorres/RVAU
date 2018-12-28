# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program acts as the preparation for the map
# It can be run on a normal or test mode

from PyQt5.QtWidgets import QApplication
import sys
import argparse
from gui.gui import MainWindow
from core.image import *


def parse_args(args):
    # If no map is given in command, quit
    if args.map is None:
        if args.test:
            print('No map loaded! Quitting...')
        quit()

    # if test flag detected
    if args.test:
        print('Starting in Test Mode!')
        print('Loading: ' + args.map + ' and related maps')

    # Get the map name without the extension
    trimmed_map_name = args.map.split('.')[0]
    return trimmed_map_name


if __name__ == '__main__':
    # Load up parameters
    # python prepare.py -m {mapfile} [-t | --test]
    parser = argparse.ArgumentParser(description="Sets up a map and its points of interest")
    parser.add_argument('-m', '--map', dest='map', default=None, type=str)
    parser.add_argument('-t', '--test', dest='test', action='store_true')

    arguments = parser.parse_args()
    map_name = parse_args(arguments)
    paths = read_image(map_name)

    # Read original image
    img = cv2.imread(paths[0])

    # Run SIFT on map image
    features = runSIFT(paths[0], map_name, arguments.test)

    app = QApplication(sys.argv)
    window = MainWindow(img, features, arguments.test, map_name)
    sys.exit(app.exec_())

