'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2B   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2b.py
*  Created:				
*  Last Modified:		8/10/2022
*  Author:				e-Yantra Team
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ PB_2931 ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_2b.py
# Functions:		control_logic, read_qr_code
# 					[ find_contours, find_contours_gray, find_centroid, deliver, rot, isnode, retspeed,  ]
# Global variables:	
# 					[  ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
##############################################################
import  sys
import traceback
import time
import os
import math
from zmqRemoteApi import RemoteAPIClient
import zmq
import numpy as np
import cv2
import random
from pyzbar.pyzbar import decode
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

def find_contours(img):
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    _, threshold = cv2.threshold(gray, 253, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_contours_gray(img):
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    _, threshold = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def find_centroid(shape):
	M=cv2.moments(shape)
	if M["m00"] !=0:
		cX=int(M["m10"]/M["m00"])
		cY=int(M["m01"]/M["m00"])
		return [cY,cX]


def deliver(sim,dropoff):
	node = ''
	package=''
	if dropoff == 1:
		node = 'checkpoint E'
		package = 'package_1'

	elif dropoff == 2:
		node = 'checkpoint I'
		package = 'package_2'

	elif dropoff == 3:
		node = 'checkpoint M'
		package = 'package_3'

	arena_dummy_handle = sim.getObject("/Arena_dummy")
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")	
	sim.callScriptFunction("activate_qr_code", childscript_handle, node)

	arena_dummy_handle = sim.getObject("/Arena_dummy")
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deliver_package", childscript_handle, package, node)

	arena_dummy_handle = sim.getObject("/Arena_dummy")
	childscript_handle = sim.getScript(sim.scripttype_childscript, arena_dummy_handle, "")
	sim.callScriptFunction("deactivate_qr_code", childscript_handle, node)


def rot(sim,count):
	s = 3.5

	joint1=sim.getObjectHandle('left_joint')
	joint2=sim.getObjectHandle('right_joint')

	if count == 0:
		for i in range(0,29):
			sim.setJointTargetVelocity(joint1,0)
			sim.setJointTargetVelocity(joint2,s)
	
	elif count==9:
		for i in range(0,29):
			sim.setJointTargetVelocity(joint1,s)
			sim.setJointTargetVelocity(joint2,0)

	elif count == 16:
		return False
	
	elif count%4 == 0:

		deliver(sim,count/4)

		for i in range(0,4):
			sim.setJointTargetVelocity(joint1,4)
			sim.setJointTargetVelocity(joint2,4)

	elif count%2 == 0:
		for i in range(0,29):
			sim.setJointTargetVelocity(joint1,0)
			sim.setJointTargetVelocity(joint2,s)
	
	elif count%2 == 1:
		for i in range(0,30):
			sim.setJointTargetVelocity(joint1,s)
			sim.setJointTargetVelocity(joint2,0)
	
	return True


def isnode(sim,img,nodecnt):
	img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	blue_lower = np.array([94, 80, 2], np.uint8)
	blue_upper = np.array([120, 255, 255], np.uint8)
	blue_mask = cv2.inRange(img2, blue_lower, blue_upper)

	res_blue = cv2.bitwise_and(img, img, mask = blue_mask)

	node = []
	cont = []
	qr = find_contours_gray(res_blue)
	
	sf=True

	if (len(qr)==13):
		for i in qr:
			node.append(cv2.contourArea(i))
			cont.append(i)
		
		maxcont = cont[node.index(max(node))]
		mid = find_centroid(maxcont)

		if mid[1] in range(190,323):
			if mid[0] in range(180,333):
				nodecnt+=1
				sf = rot(sim,nodecnt)
	
	return nodecnt,sf


def retspeed(imgcent):

	dev = int(imgcent[1]-256)

	if abs(dev) in range(1,9):
		if dev>0:
			return (0.2,0.1)
		else:
			return (0.1,0.2)

	elif abs(dev) in range(9,25):
		if dev>0:
			return (0.4,0.15)
		else:
			return (0.15,0.4)

	elif abs(dev) in range(25,57):
		if dev>0:
			return (0.6,0.2)
		else:
			return (0.2,0.6)

	elif abs(dev) in range(57,121):
		if dev>0:
			return (0.75,0.25)
		else:
			return (0.25,0.75)

	elif abs(dev) in range(121,249):
		if dev>0:
			return (0.9,0.3)
		else:
			return (0.3,0.9)

	else:
		return (1,1)

##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to make the robot follow the line to cover all the checkpoints
	and deliver packages at the correct locations.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	None

	Example call:
	---
	control_logic(sim)
	"""
	##############  ADD YOUR CODE HERE  ##############

	joint1=sim.getObjectHandle('left_joint')
	joint2=sim.getObjectHandle('right_joint')
	nodecnt = -1
	sf = True

	visionSensor = sim.getObjectHandle('vision_sensor')

	while sf == True:

		buff,res=sim.getVisionSensorImg(visionSensor)
		image = np.asarray(bytearray(buff), dtype="uint8").reshape(512,512,3)
		img = cv2.flip(image,0)

		contour = find_contours(img)
		nodecnt,sf = isnode(sim,img,nodecnt)
		
		dash=[]
		thres_area=10000
		if contour is not None:
			for cnt in contour:
				if cv2.contourArea(cnt) < thres_area:
					dash.append(cnt)

			cent = []			
			for d in dash:
				tmp=find_centroid(d)
				if tmp is not None:
					cent.append(tmp)

			ss = 4.935
			if cent is not None:

				center=list(np.mean(cent,axis=0))
				ds = retspeed(center)

				sim.setJointTargetVelocity(joint1,ds[0]*ss)
				sim.setJointTargetVelocity(joint2,ds[1]*ss)

	sim.setJointTargetVelocity(joint1,0)
	sim.setJointTargetVelocity(joint2,0)

	##################################################

def read_qr_code(sim):
	"""
	Purpose:
	---
	This function detects the QR code present in the camera's field of view and
	returns the message encoded into it.

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	`qr_message`   :    [ string ]
		QR message retrieved from reading QR code

	Example call:
	---
	control_logic(sim)
	"""
	qr_message = None
	##############  ADD YOUR CODE HERE  ##############
	visionSensor = sim.getObjectHandle('vision_sensor')
	buff,res=sim.getVisionSensorImg(visionSensor)

	image = np.asarray(bytearray(buff), dtype="uint8").reshape(512,512,3)
	img = cv2.flip(image,0)

	QR = decode(img)
	qr_message = QR[0].data.decode()

	##################################################
	return qr_message


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THE MAIN CODE BELOW #########

if __name__ == "__main__":
	client = RemoteAPIClient()
	sim = client.getObject('sim')	

	try:

		## Start the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.startSimulation()
			if sim.getSimulationState() != sim.simulation_stopped:
				print('\nSimulation started correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be started correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be started !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

		## Runs the robot navigation logic written by participants
		try:
			time.sleep(5)
			control_logic(sim)

		except Exception:
			print('\n[ERROR] Your control_logic function throwed an Exception, kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually if required.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

		
		## Stop the simulation using ZeroMQ RemoteAPI
		try:
			return_code = sim.stopSimulation()
			time.sleep(0.5)
			if sim.getSimulationState() == sim.simulation_stopped:
				print('\nSimulation stopped correctly in CoppeliaSim.')
			else:
				print('\nSimulation could not be stopped correctly in CoppeliaSim.')
				sys.exit()

		except Exception:
			print('\n[ERROR] Simulation could not be stopped !!')
			traceback.print_exc(file=sys.stdout)
			sys.exit()

	except KeyboardInterrupt:
		## Stop the simulation using ZeroMQ RemoteAPI
		return_code = sim.stopSimulation()
		time.sleep(0.5)
		if sim.getSimulationState() == sim.simulation_stopped:
			print('\nSimulation interrupted by user in CoppeliaSim.')
		else:
			print('\nSimulation could not be interrupted. Stop the simulation manually .')
			sys.exit()