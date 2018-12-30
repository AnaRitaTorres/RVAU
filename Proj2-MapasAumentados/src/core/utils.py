from cv2 import *
import numpy as np


# Serializes Key Points and their Descriptors to save them
def serialize_features(points_list, descriptors_list):
    features = []
    # Get Information From Each Key Point and store it in features array
    for point, desc in zip(points_list, descriptors_list):
        # Gets coordinates (pt), size, angle, response, octave and class id for each key point
        # Also assigns each key point to corresponding descriptor
        kp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id, desc)
        features.append(kp)

    features = np.asarray(features)
    return features


# Deserialize Key Points and their Descriptors
def deserialize_features(features):
    key_points = []
    descriptors = []

    for point in features:
        key_point = cv2.KeyPoint(x=point[0][0], y=point[0][1], _size=point[1], _angle=point[2], _response=point[3],
                                 _octave=point[4], _class_id=point[5])
        descriptor = point[6]

        key_points.append(key_point)
        descriptors.append(descriptor)

    descriptors = np.asarray(descriptors)

    return {'k': key_points, 'd': descriptors}
