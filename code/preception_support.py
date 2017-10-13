#%matplotlib qt # Choose %matplotlib qt to plot to an interactive window (note it may show up behind your browser)
# Make some of the relevant imports
import cv2 # OpenCV for perspective transform
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def color_thresh(img, rgb_thresh=(160, 160, 160)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select


# Finds the coordinates for the obstalces, and the rocks
def find_obstacles_and_rocks(img):
    return find_obstacles(img), find_rocks(img)

# Finds the rocks on the map and returns a 
# 2D matrix of 1/0 representing the rocks
def find_rocks(img):
    
    # converting to hsv
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_yellow = np.array([15, 100, 80])
    upper_yellow = np.array([100, 255, 255])
    color_select = np.zeros_like(img[:,:,0])
    
    
    rock = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
    
    thresh_map = (rock[:][:] > 0)
    
    color_select[thresh_map] = 1
    
    return color_select

# Finds the obstacles in the map and returns a 
# 2d matrix of 1/0 representing the map.
def find_obstacles(img):
    
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    upper_gray = np.array([180,160,160])
    lower_gray = np.array([0,0,0])
    color_select = np.zeros_like(img[:,:,0])
    obstacles = cv2.inRange(hsv_img, lower_gray, upper_gray)
    thresh_map = (obstacles[:][:] > 0)
    
    color_select[thresh_map] = 1
    return color_select
