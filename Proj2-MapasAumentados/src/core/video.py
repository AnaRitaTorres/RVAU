from cv2 import * 
from core.matcher import *

space_key = 32 
esc_key = 27 


# Returns a stream of video from webc amera
def captureVideo(cap, original_image): 
 
    # Read next frame 
    ret, frame = cap.read() 
 
    # Draw Center
    frame = draw_poi(frame)
    frame = matchFeatures(frame, original_image)['img']

    # Resize image a bit
    height, width, depth = frame.shape
    new_height = 1.2 * height
    new_width = 1.2 * width
    new_frame = resize(frame, (int(new_width), int(new_height)))
 
    return new_frame
