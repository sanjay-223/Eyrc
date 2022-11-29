'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 1A of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			task_1a.py
# Functions:		detect_traffic_signals, detect_horizontal_roads_under_construction, detect_vertical_roads_under_construction,
#					detect_medicine_packages, detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import cv2
import numpy as np
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

order={'Green':0,
      'Orange':1,
      'Pink':2,
      'Skyblue':3}

def checkcolor(img,color):
   return all(img[5][5] == color)


def find_shops(img):
    shop=dict()
    for i in range(6):
        shop['Shop_'+str(i+1)] = img[107:194,107+(i*100):194+(i*100)]
    return shop


def find_nodes(img):
    node = dict()
    for i in range(7):
        for j in range(7):
            node[chr(65+i)+str(j+1)] = img[94+(j*100):107+(j*100),94+(i*100):107+(i*100)]
    return node


def h_roads(img):
    h_r=dict()
    for i in range(6):
        for j in range(7):
            h_r[chr(65+i)+str(j+1)+'-'+chr(65+i+1)+str(j+1)] = img[94+(j*100):107+(j*100),107+(i*100):194+(i*100)]
    return h_r


def v_roads(img):
    v_r=dict()
    for i in range(6):
        for j in range(7):
            v_r[chr(65+j)+str(i+1)+'-'+chr(65+j)+str(i+2)] = img[107+(i*100):194+(i*100),94+(j*100):107+(j*100)]
    return v_r


def shape(no_of_vertices):
    if no_of_vertices == 3:
        return 'Triangle'
    elif no_of_vertices == 4:
        return 'Square'
    else:
        return 'Circle'

def find_color(img,centroid):
    pixel = img[centroid[1]][centroid[0]]

    if sum(pixel) == 510:
        return 'Skyblue'
    if sum(pixel) == 255:
        return 'Green'
    if sum(pixel) == 382:
        return 'Orange'
    if sum(pixel) == 435:
        return 'Pink'

def find_approx(shape):
    approx = cv2.approxPolyDP(shape, 0.025 * cv2.arcLength(shape, True), True)
    return approx  


def find_contours(shop):
    gray = cv2.cvtColor(shop,cv2.COLOR_RGB2GRAY)
    _, threshold = cv2.threshold(gray, 253, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def find_shape(no_of_vertices):
    if no_of_vertices == 3:
        return 'Triangle'
    elif no_of_vertices == 4:
        return 'Square'
    else:
        return 'Circle'

def find_centroid(shape):
    M=cv2.moments(shape)
    cX=int(M["m10"]/M["m00"])
    cY=int(M["m01"]/M["m00"])
    return [cX,cY]

def find_medicine(img):
    list_shops=[]
    shop=find_shops(img)
    for key in shop.keys():
        s_n = int(key[-1])-1
        inner_list=[]        
        contour = find_contours(shop[key])

        if len(contour)>1:
            for i in range(1,len(contour)):
                approx = find_approx(contour[i])
                
                shape = find_shape(len(approx))
                
                centroid = find_centroid(approx)
                              
                centroid[1]=centroid[1]+107
                centroid[0]=centroid[0]+107+(100*s_n)
                
                if(shape=='Triangle'):
                    centroid[0]+=1
                    centroid[1]-=1
                
                color = find_color(img,centroid)
                
                list_shops.extend([[key,color,shape,centroid]])
                
            
            list_shops.sort()
                
    return list_shops
##############################################################

def detect_traffic_signals(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list of
	nodes in which traffic signals are present in the image

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`traffic_signals` : [ list ]
			list containing nodes in which traffic signals are present
	
	Example call:
	---
	traffic_signals = detect_traffic_signals(maze_image)
	"""    
	traffic_signals = []

	##############	ADD YOUR CODE HERE	##############
	node = find_nodes(maze_image)
	for i in range(7):
		for j in range(7):
			node[chr(65+i)+str(j+1)]=cv2.cvtColor(maze_image[94+(j*100):107+(j*100),94+(i*100):107+(i*100)],cv2.COLOR_BGR2RGB)

	for key,value in node.items():
		if(checkcolor(value,[255,0,0])):
			traffic_signals.append(key)
	##################################################
	traffic_signals.sort()
	return traffic_signals
	

def detect_horizontal_roads_under_construction(maze_image):
	
	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing horizontal links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`horizontal_roads_under_construction` : [ list ]
			list containing missing horizontal links
	
	Example call:
	---
	horizontal_roads_under_construction = detect_horizontal_roads_under_construction(maze_image)
	"""    
	horizontal_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	h_r=h_roads(maze_image)
		
	for key in h_r.keys():
		if(checkcolor(h_r[key],[255,255,255])):
			horizontal_roads_under_construction.append(key)
	##################################################
	horizontal_roads_under_construction.sort()
	return horizontal_roads_under_construction	

def detect_vertical_roads_under_construction(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a list
	containing the missing vertical links

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`vertical_roads_under_construction` : [ list ]
			list containing missing vertical links
	
	Example call:
	---
	vertical_roads_under_construction = detect_vertical_roads_under_construction(maze_image)
	"""    
	vertical_roads_under_construction = []

	##############	ADD YOUR CODE HERE	##############
	v_r=v_roads(maze_image)
	
	for key,value in v_r.items():
		if(checkcolor(value,[255,255,255])):
			vertical_roads_under_construction.append(key)
	##################################################
	vertical_roads_under_construction.sort()
	return vertical_roads_under_construction


def detect_medicine_packages(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list of
	details of the medicine packages placed in different shops

	** Please note that the shop packages should be sorted in the ASCENDING order of shop numbers 
	   as well as in the alphabetical order of colors.
	   For example, the list should first have the packages of shop_1 listed. 
	   For the shop_1 packages, the packages should be sorted in the alphabetical order of color ie Green, Orange, Pink and Skyblue.

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`medicine_packages` : [ list ]
			nested list containing details of the medicine packages present.
			Each element of this list will contain 
			- Shop number as Shop_n
			- Color of the package as a string
			- Shape of the package as a string
			- Centroid co-ordinates of the package
	Example call:
	---
	medicine_packages = detect_medicine_packages(maze_image)
	"""    
	medicine_packages_present = []

	##############	ADD YOUR CODE HERE	##############
	medicine_packages_present = find_medicine(maze_image)
	##################################################

	return medicine_packages_present

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############
	arena_parameters['traffic_signals']=detect_traffic_signals(maze_image)
	arena_parameters['horizontal_roads_under_construction'] = detect_horizontal_roads_under_construction(maze_image)
	arena_parameters['vertical_roads_under_construction']=detect_vertical_roads_under_construction(maze_image)
	arena_parameters['medicine_packages_present']=detect_medicine_packages(maze_image)
	##################################################
	
	return arena_parameters

######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	

if __name__ == "__main__":

    # path directory of images in test_images folder
	img_dir_path = "public_test_images/"

    # path to 'maze_0.png' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
	
	# read image using opencv
	maze_image = cv2.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor maze_' + str(file_num) + '.png')

	# detect and print the arena parameters from the image
	arena_parameters = detect_arena_parameters(maze_image)

	print("Arena Prameters: " , arena_parameters)

	# display the maze image
	cv2.imshow("image", maze_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 15):
			
			# path to maze image file
			img_file_path = img_dir_path + 'maze_' + str(file_num) + '.png'
			
			# read image using opencv
			maze_image = cv2.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor maze_' + str(file_num) + '.png')
			
			# detect and print the arena parameters from the image
			arena_parameters = detect_arena_parameters(maze_image)

			print("Arena Parameter: ", arena_parameters)
				
			# display the test image
			cv2.imshow("image", maze_image)
			cv2.waitKey(2000)
			cv2.destroyAllWindows()