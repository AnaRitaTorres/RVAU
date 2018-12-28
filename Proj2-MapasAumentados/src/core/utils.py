from cv2 import *
import numpy as np
import pickle
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
database_path = dir_path + '/database/'


# Save Keypoints to file
def save_keypoints(filename, keypoints, descriptors, test):
    # Creates database directory
    if not os.path.exists(database_path):
        os.makedirs(database_path)

    # Serialize keypoints and their descriptors to save them in the database
    kp = serialize_keypoints(keypoints, descriptors)

    if test:
        print('\nSaving keypoints and their descriptors to file ' + filename + '_kp.bin\n');

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