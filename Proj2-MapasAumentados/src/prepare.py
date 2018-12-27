# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program acts as the preparation for the map
# It can be run on a normal or test mode

from cv2 import *
import argparse
import numpy as np

# A function to run the SIFT algorithm in the map image(s)
def runSIFT(map):
    # Read map image and convert it to grayscale
    img = imread(map)
    grayscaled = cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Run the SIFT algorithm to detect keypoints
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints = sift.detect(grayscaled, None)

    # Draw Keypoints in the image
    pointsimg = drawKeypoints(grayscaled, keypoints, img)

    # Show image and wait
    imshow('Keypoints', img)
    waitKey(5000)

# Load up parameters
# python prepare.py -m {mapfile} [-t | --test]
parser = argparse.ArgumentParser(description="Sets up a map and its points of interest")
parser.add_argument('-m', '--map', dest='map', default=None, type=str)
parser.add_argument('-t', '--test', dest='test', action = 'store_true')

args = parser.parse_args()

# if test flag detected
if (args.test):
    print('Starting in Test Mode!')
    print('Loading: ' + args.map)
    runSIFT(args.map)
if (args.map == None):
    print('No map loaded! Quitting...')
    quit()