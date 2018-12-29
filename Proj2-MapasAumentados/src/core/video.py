from cv2 import * 
from core.matcher import *

space_key = 32 
esc_key = 27 
 
# Returns a stream of video from webcamera 
def captureVideo(cap): 
 
    # Read next frame 
    ret, frame = cap.read() 
 
    # Draw Center
    frame = draw_poi(frame)

    # Resize image a bit
    height, width, depth = frame.shape
    newheight = 1.2 * height
    newwidth =  1.2 * width
    newframe = resize(frame, (int(newwidth), int(newheight)))
 
    return newframe