# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program acts as the preparation for the map
# It can be run on a normal or test mode

from cv2 import *
import argparse
import numpy as np
import re

from utils import *


# A function to run the SIFT algorithm in the map image(s)
def runSIFT(map, test):
    # Read map image and convert it to grayscale
    img = imread(map)
    grayscaled = cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Run the SIFT algorithm to detect keypoints
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(grayscaled, None)

    # Draw Keypoints in the image
    pointsimg = drawKeypoints(grayscaled, keypoints, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Save Keypoints
    save_keypoints(trimmed_map_name, keypoints, descriptors, test)

    # Show image and wait
    if test:
        print("Calculated " + str(len(keypoints)) + " keypoints in " + map)

    # Load Keypoints
    load_keypoints(trimmed_map_name, test)

    return pointsimg

# Load up parameters
# python prepare.py -m {mapfile} [-t | --test]
parser = argparse.ArgumentParser(description="Sets up a map and its points of interest")
parser.add_argument('-m', '--map', dest='map', default=None, type=str)
parser.add_argument('-t', '--test', dest='test', action='store_true')

args = parser.parse_args()

print(os.listdir('../img'))

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

# For every map in the img folder, match with the map to open and run SIFT
for m in os.listdir('..\\img\\'):
    # match map
    if re.match("" + trimmed_map_name + r"(\w)*\.\w\w\w", m):
        # Run SIFT on map image
        img = runSIFT("..\\img\\" + m, args.test)

        # Show Map
        namedWindow('Keypoints', cv2.WINDOW_NORMAL)
        imshow('Keypoints', img)

        # Wait for Key Inputs
        cv2.waitKey(0)
        destroyAllWindows()
