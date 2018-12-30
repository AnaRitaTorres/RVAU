from cv2 import *
from math import hypot

# Shows image or video with point of interest
def draw_poi(image):
    h, w, d = image.shape

    # Get Image Center
    center = (int(w/2), int(h/2))

    image = cv2.circle(image, center, 6, (0, 255, 255), -1)
    image = cv2.circle(image, center, 7, (0, 0, 0), 2)

    return image



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
        
