from cv2 import *
import numpy as np
import pickle
import os
from shutil import copy

dir_path = os.path.dirname(os.path.realpath(__file__))
database_path = dir_path + '\\database\\'
pois_path = database_path + 'POIs\\'

# Creates POI folder and file
def setupPOI(filename, test):
    # Creates POIs directory
    if not os.path.exists(pois_path):
        os.makedirs(pois_path)
    
    if test:
        print('\nSetting up Points of Interest on file ' + filename + '.txt\n')

    # Create file
    pois_file = open(pois_path + filename + '.txt', mode='wb')
    pois_file.close()

# Copy file (image) to POI folder
def copyFile(filename):
    return copy(filename, pois_path)

# Copies each POI's images to the appropriate folder, then saves all POI strings in the corresponding file
def savePOIs(filename, pois, test):

    new_pois = []
    for poi in pois:
        new_pois.append(copyImages(poi))

    # Open POIs file
    pois_file = open(pois_path + filename + '.txt', mode='wb')

    for poi in new_pois:
        if not new_pois[len(pois) - 1] == poi:
            if (test):
                print("Writing Line: " + poi)
            pois_file.write(str(poi + '\n').encode())
        else: 
            pois_file.write(poi.encode())
            print("Writing Line: " + poi)

    pois_file.close()

# Parses images from a POI string and copies them
def copyImages(poi):
    poi_split = poi.split(';')
    imgs = poi_split[3]
    imgs_split = imgs.split(',')
    new_imgs_split = []
    for img in imgs_split:
        new_imgs_split.append(copyFile(img))

    new_imgs = ','.join(new_imgs_split)
    new_poi = poi_split[0] + ';' + poi_split[1] + ';' + poi_split[2] + ';' + new_imgs
    return new_poi

# Format POI information to line (semicolumn-separated, images are comma-separated)
def formatPOI(positionx, positiony, name, imgs):
    # Create empty string
    to_return = str()

    # Add X
    to_return += str(positionx)
    to_return += ';'

    # Add Y
    to_return += str(positiony)
    to_return += ';'

    # Add POI name
    to_return += name
    to_return += ';'

    # Add images' names
    for img in imgs:
        to_return += img
        if not imgs[len(imgs) - 1] == img:
            to_return += ','

    return to_return

# Save Keypoints to file
def save_keypoints(filename, keypoints, descriptors, test):
    # Creates database directory
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    # Serialize keypoints and their descriptors to save them in the database
    kp = serialize_keypoints(keypoints, descriptors)

    if test:
        print('\nSaving keypoints and their descriptors to file ' + filename + '_kp.bin\n')

    binary_file = open(database_path + filename + '_kp.bin', mode='wb')
    pickle.dump(kp, binary_file)
    binary_file.close()


# Serializes Keypoints and their Descriptors to save them
def serialize_keypoints(keypoints_list, descriptors_list):
    keypoints = []
    # Get Information From Each Keypoint and store it in keypoints array
    for point, desc in zip(keypoints_list, descriptors_list):
        # Gets coordinates (pt), size, angle, response, octave and class id for each keypoint
        # Also assigns each keypoint to corresponding descriptor
        kp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, desc)
        keypoints.append(kp)

    keypoints = np.asarray(keypoints)
    return keypoints


# Load Keypoints From File
def load_keypoints(filename, test):
    infile = open(database_path + filename + '_kp.bin', 'rb')
    loaded = pickle.load(infile)

    # Read back keypoints from file
    results = deserialize_keypoints(loaded)

    if test:
        print('\nLoaded keypoints and their descriptors from file ' + filename + '_kp.bin');

    infile.close()


# Deserialize Keypoints and their Descriptors
def deserialize_keypoints(keypoints):
    features = []
    descriptors = []

    for point in keypoints:
        feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3],
                               _octave=point[4], _class_id=point[5])
        descriptor = point[6]

        features.append(feature)
        descriptors.append(descriptor)

    descriptors = np.asarray(descriptors)

    return {'k': features, 'd': descriptors}