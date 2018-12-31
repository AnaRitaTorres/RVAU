import cv2
from core.utils import deserialize_features
import numpy as np
from matplotlib import pyplot as plt
from math import hypot, pi, atan2, atan, cos, sin


# Shows image or video frame with highlighted point of interest and center
def draw_poi(image, pois):
    h, w, d = image.shape

    # Get Image Center
    center = (int(w/2), int(h/2))
    thickness = min(int(w/60), int(h/60))

    image = cv2.circle(image, center, thickness, (0, 255, 255), -1)
    image = cv2.circle(image, center, thickness+1, (0, 0, 0), 2)

    for poi in pois:
        center = (int(poi[0][0]), int(poi[0][1]))
        image = cv2.circle(image, center, 7, (0, 255, 0), 2)

    return image


# Draw compass on image or video frame
def draw_compass(image, angle):

    h, w, d = image.shape
    displacement = 50

    # Offset of Compass
    if w > h or w == h:
        r = int(w/2) + displacement
        d = int(h/2)
    else:
        r = int(w/2)
        d = int(h/2) + displacement

    c = cos(angle)
    s = sin(angle) 

    # Upper Part of Compass
    compass_north = np.array([[[r-int(10*c), d-int(10*s)], [r+int(10*c), d+int(10*s)], [r+int(30*s), d-int(30*c)]]])

    # Lower part of Compass
    compass_south = np.array([[[r-int(10*c), d-int(10*s)], [r+int(10*c), d+int(10*s)], [r-int(30*s), d+int(30*c)]]])

    # Filled Portion
    image = cv2.fillConvexPoly(image, compass_north, (0,0,255),lineType = 8, shift = 0)
    image = cv2.fillConvexPoly(image, compass_south, (255,0,0),lineType = 8, shift = 0)

    return image


# Find SIFT features in image and compare them to original image's features
def matchFeatures(image, original_image, test):

    MIN_MATCH_COUNT = 10

    # Read original image
    original_img = cv2.imread(original_image.filename)

    # Convert imgs to grayscale
    grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscaled_original = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # Run SIFT on image, get original's
    sift = cv2.xfeatures2d.SIFT_create(250)
    keypoints_image, descriptors_image = sift.detectAndCompute(grayscaled_image, None)
    or_arr = deserialize_features(original_image.features)

    # Extract keypoints from dictionary
    keypoints_original, descriptors_original = or_arr['k'], or_arr['d']

    # If either image does not have any descriptors
    if descriptors_image is None or descriptors_original is None:
        return {'img': image, 'pts': None, 'dst': None, 'angle': None, 'matrix': None}

    # Run Flann Based Matcher to find matches
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    if len(keypoints_image) > 1 and len(or_arr['k']) > 1:
        matches = flann.knnMatch(descriptors_original, descriptors_image, k=2)
    else:
        return {'img': image, 'pts': None, 'dst': None, 'angle': None, 'matrix': None}

    # Matches go here
    good = []

    for m, n in matches:
        
        # Filter out bad matches
        if m.distance < 0.7 * n.distance:
            good.append(m)

    matches.clear()

    # If there are at least MIN_MATCH_COUNT matches
    if len(good) > MIN_MATCH_COUNT:

        # Reshape keypoints to find homography
        src_pts = np.float32([ keypoints_original[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoints_image[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        # Find the homography between source and destination
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h, w, depth = original_img.shape

        # Get new src and destination points
                
        try:
            pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
            dst = cv2.perspectiveTransform(pts,M)

            # Redraw original image to show where the test image is
            image = cv2.polylines(image, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

            return {'img': image, 'pts': pts, 'dst': dst, 'angle': calculateAngle(dst[1][0], dst[0][0]), 'matrix': M}
        except:
            return {'img': image, 'pts': None, 'dst': None, 'angle': None, 'matrix': None}
    # Not enough good matches
    else:
        if test:
            print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            matchesMask = None

    return {'img': image, 'pts': None, 'dst': None, 'angle': None, 'matrix': None}


# Calculate the angle of the vector between two points
def calculateAngle(pt1, pt2):
    doublepi = pi * 2
    rad2deg = 57.2957795130823209
    
    theta = atan2(pt2[0] - pt1[0], pt2[1] - pt1[1])
    if theta < 0.0:
        theta += doublepi
    return -(theta - pi)


# Calculate point of interest perspective
def poi_perspective(pois, M):
    arr = []
    arr.append(pois)

    pts = np.float32(arr).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    return dst


# Get points of interest
def get_pois(pts, M):
    pois = []

    for pt in pts:
        pois.append([pt.position_x, pt.position_y])

    new_pois = poi_perspective(pois, M)

    return new_pois
