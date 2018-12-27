from cv2 import *
import numpy as np
import pickle

filename = 'map.bin'

def save_keypoints(keypoints, descriptors):
    kp = serialize_keypoints(keypoints, descriptors)

    binary_file = open(filename, mode='wb')
    pickle.dump(kp, binary_file)
    binary_file.close()


# Serializes Keypoints and their Descriptors to save them in map.bin
def serialize_keypoints(keypoints_list, descriptors_list):
    print(keypoints_list[0].pt)
    print(descriptors_list[0])

    keypoints = []
    # Get Information From Each Keypoint and store it in keypoints array
    for point, desc in zip(keypoints_list, descriptors_list):
        kp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, desc)
        keypoints.append(kp)

    keypoints = np.asarray(keypoints)
    return keypoints


# Load Keypoints From File
def load_keypoints():
    infile = open(filename, 'rb')
    loaded = pickle.load(infile)
    results = deserialize_keypoints(loaded)

    print(results['k'][0].pt)
    print(results['d'][0])

    infile.close()


# Deserialize Keypoints and their Descriptors
def deserialize_keypoints(keypoints):
    features = []
    descriptors = []

    for point in keypoints:
        temp_feature = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3],
                                    _octave=point[4], _class_id=point[5])
        temp_descriptor = point[6]

        features.append(temp_feature)
        descriptors.append(temp_descriptor)

    descriptors = np.asarray(descriptors)

    return {'k': features, 'd': descriptors}
