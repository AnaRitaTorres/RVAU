from cv2 import * 
from core.matcher import *

space_key = 32 
esc_key = 27 


# Returns a stream of video from web camera
def captureVideo(cap, mode, original_image, scale, test):
 
    # Read next frame 
    ret, frame = cap.read() 
 
    arr = matchFeatures(mode, frame, original_image, test)

    point_of_interest = original_image.points[0]
    distance = 0

    if arr['img'] is not None:
        frame = arr['img']
    if arr['angle'] is not None:
        frame = draw_compass(frame, arr['angle'])
    if arr['matrix'] is not None:
        p_arr = get_pois(original_image.points, arr['matrix'])
        results = draw_poi(frame, p_arr, scale)

        frame = results['img']
        point_of_interest = results['point']
        distance = results['distance']

    # Resize image a bit
    height, width, depth = frame.shape
    new_height = 1.2 * height
    new_width = 1.2 * width
    new_frame = resize(frame, (int(new_width), int(new_height)))

    return {'img': new_frame, 'point': point_of_interest, 'distance': distance}
