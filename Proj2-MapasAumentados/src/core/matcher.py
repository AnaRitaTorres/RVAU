from cv2 import *
from core.utils import *
import numpy as np
from matplotlib import pyplot as plt
from math import hypot, pi, atan2, atan, cos, sin

# Shows image or video with point of interest
def draw_poi(image):
    h, w, d = image.shape

    # Get Image Center
    center = (int(w/2), int(h/2))

    image = cv2.circle(image, center, 13, (0, 255, 255), -1)
    image = cv2.circle(image, center, 14, (0, 0, 0), 2)

    return image

def draw_compass(image, angle):

    h, w, d = image.shape

    displacement_down = 15
    displacement_right = 35

    # Offset of Compass
    r = int(w/2) + displacement_right
    d = int(h/2) + displacement_down

    c = cos(angle)
    s = sin(angle) 

    # Upper Part of Compass
    compassNorth = np.array([[[r-int(10*c),d-int(10*s)],[r+int(10*c),d+int(10*s)],[r+int(30*s),d-int(30*c)]]])

    # Lower part of Compass
    compassSouth = np.array([[[r-int(10*c),d-int(10*s)],[r+int(10*c),d+int(10*s)],[r-int(30*s),d+int(30*c)]]])

    # Filled Portion
    image = cv2.fillConvexPoly(image, compassNorth, (0,0,255),lineType = 8, shift = 0)
    image = cv2.fillConvexPoly(image, compassSouth, (255,0,0),lineType = 8, shift = 0)

    return image


# Find SIFT features in image and compare them to original image's features
def matchFeatures(image, original_image, test):

    MIN_MATCH_COUNT = 10

    # Read original image
    original_img = imread(original_image.filename)

    # Convert imgs to grayscale
    grayscaled_image = cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscaled_original = cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # Run SIFT on image, get original's
    sift = cv2.xfeatures2d.SIFT_create(250)
    keypoints_image, descriptors_image = sift.detectAndCompute(grayscaled_image, None)
    or_arr = deserialize_features(original_image.features)

    # Extract keypoints from dictionary
    keypoints_original, descriptors_original = or_arr['k'], or_arr['d']

    # Run Flann Based Matcher to find matches
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(descriptors_original, descriptors_image, k=2)

    # Matches go here
    good = []

    for m,n in matches:
        
        # Filter out bad matches
        if m.distance < 0.5 * n.distance:
            good.append(m)

    # If there are at least MIN_MATCH_COUNT matches
    if len(good)>MIN_MATCH_COUNT:

        # Reshape keypoints to find homography
        src_pts = np.float32([ keypoints_original[m.queryIdx].pt for m in good]).reshape(-1,1,2)
        dst_pts = np.float32([ keypoints_image[m.trainIdx].pt for m in good]).reshape(-1,1,2)

        # Find the homography between source and destination
        M, mask = findHomography(src_pts, dst_pts, RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h,w,depth = original_img.shape

        # Get new src and destination points
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = perspectiveTransform(pts,M)

        # Redraw orignal image to show where the test image is
        image = polylines(image, [np.int32(dst)],True,255,3, LINE_AA)

        return {'img': image, 'pts': pts, 'dst': dst, 'angle': calculateAngle(dst[1][0], dst[0][0])}
    # Not enough good matches
    else:
        if test:
            print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            matchesMask = None

    return {'img':image, 'pts': None, 'dst': None, 'angle': None}

# Calculate the angle of the vector between two points
def calculateAngle(pt1, pt2):
    doublepi = pi * 2
    rad2deg = 57.2957795130823209
    
    theta = atan2(pt2[0] - pt1[0], pt2[1] - pt1[1])
    if theta < 0.0:
        theta += doublepi
    return -(theta -pi)

# Calculates the linear distance between the 2 points
def linear_distance(x1,y1,x2,y2):

    #distance calculation
    dist = math.hypot(x2 - x1, y2 - y1)

    return dist

# Calculates distance to all interest points and returns the closest one
def closest_POI(x1,y1,pois):

    all_dist = []

    for poi in pois:
        dist = linear_distance(x1,y1,poi[0],poi[1])
        all_dist.append(dist)

    # get min dist point coords
        
