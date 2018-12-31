from core.utils import *


# A function to run the SIFT algorithm in the map image(s)
def runSIFT(map, test):
    # Read map image and convert it to grayscale
    img = imread(map)
    grayscaled = cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Run the SIFT algorithm to detect keypoints
    sift = cv2.xfeatures2d.SIFT_create(3000)
    keypoints, descriptors = sift.detectAndCompute(grayscaled, None)

    # Draw Key points in the image
    points_img = drawKeypoints(img, keypoints, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Serialized Features
    features = serialize_features(keypoints, descriptors)

    # Show Image and wait
    if test:
        print("Calculated " + str(len(keypoints)) + " keypoints in " + map)

    return {'img_features': points_img, 'pts_features': features}

# A function to run the ORB algorithm in the map image(s)
def runORB(map, test):
    # Read map image and convert it to grayscale
    img = imread(map)
    grayscaled = cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Run the ORB algorithm to detect keypoints
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(grayscaled, None)

    # Draw Key points in the image
    points_img = drawKeypoints(img, keypoints, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Serialized Features
    features = serialize_features(keypoints, descriptors)

    # Show Image and wait
    if test:
        print("Calculated " + str(len(keypoints)) + " keypoints in " + map)

    return {'img_features': points_img, 'pts_features': features}
