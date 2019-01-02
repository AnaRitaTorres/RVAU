import cv2
import numpy as np
from matplotlib import pyplot as plt
from math import hypot, pi, atan2, atan, cos, sin
from core.utils import deserialize_features
from core.database import PointOfInterest


# Shows image or video frame with highlighted point of interest and center
def draw_poi(image, pois, scale):
    h, w, d = image.shape

    # Get Image Center
    center = (int(w/2), int(h/2))
    thickness = min(int(w/85), int(h/85))

    image = cv2.circle(image, center, thickness, (0, 255, 255), -1)
    image = cv2.circle(image, center, thickness + 1, (0, 0, 0), 2)

    result = closest_POI(center[0], center[1], pois)

    if result['point'] is None:
        point_of_interest = None
        distance = 0
    else:
        point_of_interest = result['point']
        pixels = int(result['distance'])

        # Convert pixels to centimeters
        centimeters = pixels * 2.54 / 96
        scale = float(scale)
        distance = int(centimeters * scale)

        center = (point_of_interest.position_x, point_of_interest.position_y)
        image = cv2.circle(image, center, thickness+2, (0, 255, 0), -1)
        image = cv2.circle(image, center, thickness+3, (0, 0, 0), 2)

    return {'img': image, 'point': point_of_interest, 'distance': distance}


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
def matchFeatures(mode, image, original_image, test):

    if mode == 'image':
        MIN_MATCH_COUNT = 100
    else:
        MIN_MATCH_COUNT = 10

    # Read original image
    original_img = cv2.imread(original_image.filename)

    # Convert imgs to grayscale
    grayscaled_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscaled_original = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # Run SIFT on image, get original's
    if mode == 'image':
        sift = cv2.xfeatures2d.SIFT_create(2000)
    else:
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
def get_pois(img, pts, M):
    points = []
    pois = []

    h, w, d = img.shape

    for pt in pts:
        points.append([pt.position_x, pt.position_y])

    new_points = poi_perspective(points, M)

    for pt, poi in zip(new_points, pts):
        position_x = int(pt[0][0])
        position_y = int(pt[0][1])

        if position_y > 0 and position_y > 0:
            if position_x < w and position_y < h:
                point = PointOfInterest(position_x, position_y, poi.name, poi.images)
                pois.append(point)

    return pois


# Calculates the linear distance between the 2 points
def linear_distance(x1, y1, x2, y2):

    # Distance calculation
    dist = hypot(x2 - x1, y2 - y1)

    return dist


# Calculates distance to all interest points and returns the closest one
def closest_POI(x1, y1, pois):
    if len(pois) > 0:
        all_dist = []

        for poi in pois:
            dist = linear_distance(x1, y1, poi.position_x, poi.position_y)
            all_dist.append({'point': poi, 'dist': dist})

        # get min dist point coords
        result = min(all_dist, key=lambda x: x['dist'])
    else:
        result = {'point': None, 'dist': 0}

    return {'point': result['point'], 'distance': result['dist']}

