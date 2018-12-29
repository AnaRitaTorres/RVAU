# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program takes an image feed and pinpoints points of interest
# It can be run on a normal or test mode

import sys
import argparse
from PyQt5.QtWidgets import QApplication
from core.matcher import *
from core.detector import *
from gui.gui_augment import MainWindow

# python augment.py image -m 'london_tourist_map_rotate.jpg' -o 'london_tourist_map.jpg' -t'
# python augment.py video -o 'london_tourist_map.jpg' -t

def parse_args_image(args):
    if args.map is None:
        print('No map loaded! Quitting...')
        quit()

    if args.original_map is None:
        print('No original map given! Quitting...')
        quit()

    print('Loading: ' + args.map)

    trimmed_map_name = args.map.split('.')[0]
    loadedmap = read_image(trimmed_map_name)[0]

    # Read image
    img = imread(loadedmap)

    img = draw_poi(img)

    # Create window map    
    app = QApplication(sys.argv)
    window = MainWindow('image', img, arguments.test)
    sys.exit(app.exec_())


def parse_args_video():

    if args.original_map is None:
        print('No original map given! Quitting...')
        quit()

    print('Streaming video...')
    app = QApplication(sys.argv)
    window = MainWindow('video', None, arguments.test)
    sys.exit(app.exec_())


if __name__ == '__main__':
    # Load up parameters
    # python prepare.py [video|img] -m {mapfile} [-t | --test]
    parser = argparse.ArgumentParser(description="Sets up a map and its points of interest")
    parser.add_argument('method', help='\'video\' or \'image\'', type=str)
    parser.add_argument('-m', '--map', dest='map', default=None, type=str)
    parser.add_argument('-o', '--original_map', dest='original_map', default=None, type=str)
    parser.add_argument('-t', '--test', dest='test', action = 'store_true')

    arguments = parser.parse_args()

    # If test flag detected
    if arguments.test:
        print('Starting in Test Mode!')

    if arguments.method == 'image':
        parse_args_image(arguments)
   
    else:
        parse_args_video()
    

