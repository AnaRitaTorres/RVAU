# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program takes an image feed and pinpoints points of interest
# It can be run on a normal or test mode

from cv2 import *
import argparse
from core.video import *
from core.matcher import *

# python augment.py image -m 'london_tourist_map.jpg' -t


def parse_args_image(args):
    if args.map is None:
        print('No map loaded! Quitting...')
        quit()

    print('Loading: ' + args.map)

    # Read image
    img = imread(args.map)

    img = draw_poi(img)

    # Create window map
    # TODO: Use PyQt5 to show this stuff
    namedWindow('Map', cv2.WINDOW_NORMAL)
    cv2.imshow('Map', img)

    waitKey(0)


def parse_args_video():
    print('Streaming video...')
    capture_video()


if __name__ == '__main__':
    # Load up parameters
    # python prepare.py [video|img] -m {mapfile} [-t | --test]
    parser = argparse.ArgumentParser(description="Sets up a map and its points of interest")
    parser.add_argument('method', help='\'video\' or \'image\'', type=str)
    parser.add_argument('-m', '--map', dest='map', default=None, type=str)
    parser.add_argument('-t', '--test', dest='test', action = 'store_true')

    arguments = parser.parse_args()

    # If test flag detected
    if arguments.test:
        print('Starting in Test Mode!')

    if arguments.method == 'image':
        parse_args_image(arguments)
    else:
        parse_args_video()
   
    

