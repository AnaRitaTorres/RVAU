# RVAU 2018/19
# Second Practical Project - Augmented Maps
# by Ana Rita Torres, Cláudia Marinho, Rui Soares

# This program takes an image feed and pinpoints points of interest
# It can be run on a normal or test mode

from cv2 import *
import argparse
from core.video import *

# python augment.py image -m 'london_tourist_map.jpg' -t

def parse_args_image(args):
    # If test flag detected
    if (args.test):
        print('Starting in Test Mode!')
        if (args.method == 'image'):        
            if (args.map == None):
                print('No map loaded! Quitting...')
                quit()
            print('Loading: ' + args.map)

def parse_args_video(args):
    if (args.method == 'video'):
        print('Streaming video...')
        CaptureVideo()

if __name__ == '__main__':
    # Load up parameters
    # python prepare.py [video|img] -m {mapfile} [-t | --test]
    parser = argparse.ArgumentParser(description="Sets up a map and its points of interest")
    parser.add_argument('method' ,help='\'video\' or \'image\'', type=str)
    parser.add_argument('-m', '--map', dest='map', default=None, type=str)
    parser.add_argument('-t', '--test', dest='test', action = 'store_true')

    arguments = parser.parse_args()
    image = parse_args_image(arguments)
    video = parse_args_video(arguments)
   
    

