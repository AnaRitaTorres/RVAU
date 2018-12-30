import pickle
import os.path
import shutil
from core.utils import *
from core.detector import *

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


# Represents a Map. Initialize with name of the entry, map scale and filename of the frontal image
# Also associated to a set of one or more images
class MapEntry:
    def __init__(self, name, scale, frontal_image, images):
        self.name = name
        self.scale = scale
        self.frontal_image = frontal_image
        self.images = images


# Returns a list with the names of the maps currently stored in database
def get_map_names(maps):
    map_names = []

    for map_entry in maps:
        map_names.append(map_entry.name)

    return map_names


# Returns map information from the database given a map name and a set of maps
def get_map(map_name, maps):
    for map_entry in maps:
        if map_name == map_entry.name:
            return map_entry

    return None


# Get base image information
def get_base_image(map_entry):
    filename = map_entry.frontal_image

    for image in map_entry.images:
        if image.filename == filename:
            return image


# Loads database if it exists and prints their contents
def load_database():
    empty_map = []
    # Check if database exists
    if not os.path.isfile(database_name):
        print("Database doesn't yet exist")
        return empty_map

    infile = open(database_name, 'rb')
    maps = pickle.load(infile)
    infile.close()

    for map_entry in maps:
        print('\nMap name:', map_entry.name)
        print('\nMap scale:', map_entry.scale)
        print('\nFrontal image of map:', map_entry.frontal_image)

        for img in map_entry.images:
            print('\nImage name:', img.filename)
            features = deserialize_features(img.features)
            print('Deserialized features:', len(features['k']), len(features['d']), 'points')

            for poi in img.points:
                print('Point of Interest:', poi.position_x, poi.position_y, poi.name, poi.images)

    print('\n')

    return maps


# Check if database exists and update its contents if it exists
def update_database(entry_name, map_scale, filename, images):
    # List of maps to be added to the database
    maps = []

    # Creates current map entry
    map_entry = MapEntry(entry_name, map_scale, filename, images)

    # Check if database exists
    if os.path.isfile(database_name):

        # Read database contents
        infile = open(database_name, 'rb')
        maps_loaded = pickle.load(infile)

        # Boolean used to check if map already exists on the database
        map_exists = False

        # Iterate over maps already on the database
        for i in range(len(maps_loaded)):
            # Checks if there is an map in database equal to current one
            if maps_loaded[i].name == entry_name:
                # Equal map exists
                map_exists = True

                # Update images of map found on the database
                maps_loaded[i].images = images

        # Checks after iterating over maps if current map doesn't exist in database
        if not map_exists:
            maps_loaded.append(map_entry)

        # Get updated map
        maps = maps_loaded
    else:
        # If database doesn't exist, just append map entry
        maps.append(map_entry)

    return maps


# Saves map to database
def save_database(entry_name, map_scale, filename, more_images, features, pois, test):
    # Get points with new file paths
    points = setup_pois(pois)

    images = []

    for p in points:
        print('Points', p.name, p.position_x, p.position_x, p.images)

    for img_filename in more_images:
        # Run SIFT on map image
        results = runSIFT(img_filename, test)

        new_image = Image(img_filename, results['pts_features'], [])

        images.append(new_image)

    # Create image object
    image = Image(filename, features, points)

    images.append(image)
    maps = update_database(entry_name, map_scale, filename, images)

    # Save images to database
    binary_file = open(database_name, mode='wb')
    pickle.dump(maps, binary_file)
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
    img = filename
    try:
        img = shutil.copy(filename, points_path)
    except shutil.SameFileError:
        print("Copying same file to folder")

    return img
