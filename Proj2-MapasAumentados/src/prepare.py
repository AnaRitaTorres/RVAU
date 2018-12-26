# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program acts as the preparation for the map
# It can be run on a normal or test mode

from cv2 import *
import argparse

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
if (args.map == None):
    print('No map loaded! Quitting...')
    quit()