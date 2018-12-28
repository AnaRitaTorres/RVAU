from cv2 import *

space_key = 32
esc_key = 27


# Returns a stream of video from web camera
def capture_video():

    # Start Video Capture
    cap = VideoCapture(0)

    # Current Frame
    img = None

    # Video Loop
    while True:

        # Read next frame
        ret, frame = cap.read()
        
        # Show frame
        imshow('frame', frame)

        # Wait for Space or Esc key press
        key = waitKey(1)
        if key == space_key:
            img = frame
            break
        if key == esc_key:
            break

    # End Capture
    cap.release()
    
    # Close windows
    destroyAllWindows()

    return img
