import pickle
import os.path
from shutil import copy
from core.utils import *

database_name = 'maps.db'
points_path = 'POIs\\'


# Represents a Point of Interest. Initialize with point coordinates (x and y), name given by user and array of images
class PointOfInterest:
    def __init__(self, position_x, position_y, name, images):
        self.position_x = position_x
        self.position_y = position_y
        self.name = name
        self.images = images


# Represents an Image. Initialize with filename, features and points of interest as arguments
class Image:
    def __init__(self, filename, features, points):
        self.filename = filename
        self.features = features
        self.points = points


# Loads database if it exists and prints their contents
def load_database():
    # Check if database exists
    if not os.path.isfile(database_name):
        print("Database doesn't yet exist")
        return

    infile = open(database_name, 'rb')
    images = pickle.load(infile)
    infile.close()

    for img in images:
        print('\nImage name:', img.filename)
        features = deserialize_features(img.features)
        print('Deserialized features:', len(features['k']), len(features['d']), 'points')

        for poi in img.points:
            print('Point of Interest:', poi.position_x, poi.position_y, poi.name, poi.images)

    print('\n')


# Check if database exists and update its contents if it exists
def update_database(filename, image):
    images = []

    # Check if database exists
    if os.path.isfile(database_name):
        # Read database contents
        infile = open(database_name, 'rb')
        images_loaded = pickle.load(infile)
        img_exists = False

        for i in range(len(images_loaded)):
            # If there is an image in database equal to current one, update it
            if images_loaded[i].filename == filename:
                images_loaded[i] = image
                img_exists = True
                print('Current image already exists in database')

        # Append the rest of content
        images = images + images_loaded

        # If current image doesn't exist, append it
        if not img_exists:
            images.append(image)
    else:
        # If database doesn't exist, just append current image
        images.append(image)

    return images


# Saves image to database
def save_database(filename, features, pois):
    # Get points with new file paths
    points = setup_pois(pois)

    for p in points:
        print('Points', p.name, p.position_x, p.position_x, p.images)

    # Create image object
    image = Image(filename, features, points)
    images = update_database(filename, image)

    # Save images to database
    binary_file = open(database_name, mode='wb')
    pickle.dump(images, binary_file)
    binary_file.close()


# Copies each POI's images to the appropriate folder, then returns all POIs
def setup_pois(pois):
    # Creates POIs directory
    if not os.path.exists(points_path):
        os.makedirs(points_path)

    # Iterate over points of interest and get their new paths
    new_points = []
    for poi in pois:
        new_points.append(copy_images(poi))

    print('Copied all POI images to new folder')

    # Return updated points of interest
    return new_points


# Parses images from a PointOfInterest object and copies them to a new folder
def copy_images(poi):
    # Get images attached to Point of Interest
    poi_images = poi.images

    # Iterate over images, copy them to new folder and get their path
    new_images = []
    for img in poi_images:
        new_images.append(copy_file(img))

    # Update image paths in Point of Interest object
    poi.images = new_images
    return poi


# Copy image to Points of Interests folder
def copy_file(filename):
    return copy(filename, points_path)
