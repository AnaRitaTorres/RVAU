from cv2 import * 
from core.matcher import *

space_key = 32 
esc_key = 27 


# Returns a stream of video from webc amera
def captureVideo(cap, original_image, test): 
 
    # Read next frame 
    ret, frame = cap.read() 
 
    arr = matchFeatures(frame, original_image, test)
    if arr['img'] is not None:
        frame = arr['img']
    if arr['angle'] is not None:
        frame = draw_compass(frame, arr['angle'])
    if arr['matrix'] is not None:
        p_arr = get_pois(original_image.points,arr['matrix'])
        frame = draw_poi(frame, p_arr)
    # Resize image a bit
    height, width, depth = frame.shape
    new_height = 1.2 * height
    new_width = 1.2 * width
    new_frame = resize(frame, (int(new_width), int(new_height)))
 
    return new_frame
