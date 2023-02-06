'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy 
from  numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################

mtx = numpy.array([[527.62824681,   0,         285.54028664],
 [  0,         537.21865006, 257.10786103],
 [  0,          0,           1        ]])

newcameramtx = mtx

dist = numpy.array([[-6.32256328e-01,  8.16753364e-01,  8.07936800e-04,  2.23713609e-02,
  -1.15661431e+00]])


aruco_details = []  

def distance(p1,p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5


def transform_coord(x,y):
    a = (x * 1.90)/512  + (-0.95)
    b = (y * 1.90)/512 + (-0.95)
    return a,-b


def transform_angle(angle):
    if angle>0:
        theta= (angle-180) * ((3.14159)/180)
    else:
        theta= (angle+180) * ((3.14159)/180)
    return theta
        
def get_perspective_parameters(img):
    try:
        ad,_ = task_1b.detect_ArUco_details(img)
        p1 = [ad[3][0],ad[4][0],ad[2][0],ad[1][0]]

        return p1
    except:
        return None

def gettransformed_image(img):
    h,  w = img.shape[:2]
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, mtx, (w,h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    h,w = 512,512
    #get Transformation matrix
    pts1 = numpy.float32(get_perspective_parameters(dst))
    pts2 = numpy.float32([[0,0],[h-1,0],[0,w-1],[h-1,w-1]])
    

    #warping the image
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(dst, matrix, (h,w))

    return result




#####################################################################################

def perspective_transform(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = [] 
#################################  ADD YOUR CODE HERE  ###############################
    warped_image = gettransformed_image(image)
######################################################################################

    return warped_image

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################
    aruco_details = task_1b.detect_ArUco_details(image)
    ar5=aruco_details[0][5]
    x,y= transform_coord(ar5[0][0],ar5[0][1])
    theta = transform_angle(ar5[1])
    scene_parameters.append(x)
    scene_parameters.append(y)
    scene_parameters.append(theta)
######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################
    arena_handle = sim.getObject('/Arena')
    sim.setObjectPosition(aruco_handle,arena_handle,[scene_parameters[0],scene_parameters[1],0.03])
    sim.setObjectOrientation(aruco_handle,arena_handle,[0,0,scene_parameters[2]+3.14159])
######################################################################################

    return None


if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
#################################  ADD YOUR CODE HERE  ################################
   
    cam = cv2.VideoCapture(0)
    while True:
        _,img = cam.read()
        cv2.imshow('frame',img)
        cv2.waitKey(1)
        try:
            ad,_ = task_1b.detect_ArUco_details(img)
            result = perspective_transform(img)
            scene_parameters = transform_values(result)   
            set_values(scene_parameters)
        except:
            continue
    
    cv2.destroyAllWindows() 
#######################################################################################



    
