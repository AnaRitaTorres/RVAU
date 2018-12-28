import re
from core.utils import *


# A function to run the SIFT algorithm in the map image(s)
def runSIFT(map, name, test):
    # Read map image and convert it to grayscale
    img = imread(map)
    grayscaled = cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Run the SIFT algorithm to detect keypoints
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(grayscaled, None)

    # Draw Key points in the image
    points_img = drawKeypoints(img, keypoints, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Serialized Features
    features = serialize_features(keypoints, descriptors)

    # Show Image and wait
    if test:
        print("Calculated " + str(len(keypoints)) + " keypoints in " + map)

    return {'img_features': points_img, 'pts_features': features}


# Get array of maps matching map name
def read_image(map_name):
    # Array for all maps in the img folder
    paths = []

    # For every map in the img folder, match with the map
    for m in os.listdir('..\\img\\'):
        # match map
        if re.match("" + map_name + r"(\w)*\.\w\w\w", m):
            #
            file_path = "..\\img\\" + m
            paths.append(file_path)

    return paths

