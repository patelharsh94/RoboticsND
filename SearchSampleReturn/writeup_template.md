## Project: Search and Sample Return
### Writeup Template: You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[rock_image]: ./calibration_images/example_rock1.jpg 
[before_perspective_transform]: ./calibration_images/example_grid1.jpg
[after_perspective_transform]: ./calibration_images/after_prespective_transform.png
[after_color_thresh]: ./calibration_images/after_color_thresh.png
[after_find_obstacles]: ./calibration_images/after_find_obstacles.png
[after_find_rock]: ./calibration_images/after_find_rock.png

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  


### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Perspective transform: 
In order to perform a perspective transform I used the function 
`perspect_transform()`:
In this function I defined source as :
`source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])`
and destination as:
`destination = np.float32([[image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])`


####Before:
![before_perspective_transform] 
####After: ![after_perspective_transform]

                  
         
                  

In order to perform proper threshold and color selection  I had modified/written 3 functions.  
1.) `color_thresh()`:
    This function was primarily for recognizing nagivable terrain.
    The threshold value I used to tell the difference between navigable terrain,
    and mountains was 160,160,160.
    
#####Before:
![after_perspective_transform] 
#####After:
![after_color_thresh]
    
2.) Find obstacles; In order to find obstacles I decided to use the function `find_obstacles()`
    For the following two functions I decided to use open cv ranginging and image transformation functions.
   
   I set the higher color values to be [180,160,160]
   and the lower color value to be [0,0,0]
   
   And found colors on the map that represent the mountain.  It's basically the inverse of the previous function.
   I decide to change the color values from rgb to hsv just to get more experience using opencv and
   it's built in functions.
####Before:
![after_perspective_transform]    
####After:
![after_find_obstacles]
`as you can see, the parts of the picture that were black in the prvious picture, are white now. 
 And vice versa. `

3.) Find Rocks: In order to find rocks, I used the same techinique as above.
   I set the higher color values to be [15, 100, 80]
   and the lower color value to be [100, 255, 255]
####Before:
![rock_image]
####After
![after_find_rock]

** I wrote a helper function called find_obstacle_and_rock() to call both the above function and return
the respective image.

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

For the process image function, I followed the steps that were commented.
* I got the warped image using the perspective_transform() function. 
* I called color_thresh() and find_obstacle_and_rock() to get a color coded image.
* I called the rover_coordinate() function to get the location of the obstacles and rocks.
* Then I called pix_to_world() to get the pixel locations
* Finally I overlaid the locations onto the world map, changing channels for the 3 different scenario  
### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.
__Perception Step__
For the perception step I stuck to the process I came up with in the process_image() function,
but changed the world map overlay to re-assigning new values to the Rover object.

__Decision Step__
In the decision_step I kept the code similar to what was already given, with the majority
of changes made under the condition `Rover.mode == 'stop'`  The general approach to getting unstuck,
was to stop and rotate, until more navigable terrain was found. In one case, where no possible solution was 
in sight, the robot will go back until more navigable terrain was found.

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  

__Note: My approach is mentioned above.__
__What Worked__ 
I used the opencv function `cv2.inRange()` to find the difference between obstacles, road and rocks.  It worked out to be 
an easier and simpler to understand implementation. 
__Improvements__

* I might not convert the image to hvs from rgb for the threshold, just because the over all lighting was not varying on the map.
* I would like to replace my implementation of the decision_step() by removing the if-else and replacing it with a 
  state machine implementation.  The logic implemented by other students make the robot much simpler to understand,
  edit, and improve.  It allowed for more complex decision making and more complex functionality. 
* I would figure out a better way of making the robot 'wall hugging'
* I would add functionality for picking up rocks.



