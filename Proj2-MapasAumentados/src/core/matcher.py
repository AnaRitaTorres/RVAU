from cv2 import *


# Shows image or video with point of interest
def draw_poi(image):
    h, w, d = image.shape

    # Get Image Center
    center = (int(w/2), int(h/2))

    image = cv2.circle(image, center, 11, (0, 255, 255), -1)
    image = cv2.circle(image, center, 12, (0, 0, 0), 2)

    return image
