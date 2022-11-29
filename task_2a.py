'''
*****************************************************************************************
*
*        =================================================
*             Pharma Bot Theme (eYRC 2022-23)
*        =================================================
*                                                         
*  This script is intended for implementation of Task 2A   
*  of Pharma Bot (PB) Theme (eYRC 2022-23).
*
*  Filename:			task_2a.py
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

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_2a.py
# Functions:		control_logic, detect_distance_sensor_1, detect_distance_sensor_2
# 					[ Comma separated list of functions in this file ]
# Global variables:	
# 					[ List of global variables defined in this file ]

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
##############################################################

def control_logic(sim):
	"""
	Purpose:
	---
	This function should implement the control logic for the given problem statement
	You are required to actuate the rotary joints of the robot in this function, such that
	it traverses the points in given order

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
	speed = 1.075
	dist2 = detect_distance_sensor_2(sim)
	dist3 =  detect_distance_sensor_3(sim)
	d = dist2 +0.16
	Stop=False
	while not Stop:
		dist1 = detect_distance_sensor_1(sim)
		dist2 = detect_distance_sensor_2(sim)
		dist3 = detect_distance_sensor_3(sim)
		  
    

		joint1=sim.getObjectHandle('left_joint')
		joint2=sim.getObjectHandle('right_joint')

		


		
		if dist1 == 0 or dist1 > d :
			
			sim.setJointTargetVelocity(joint1,5)
			sim.setJointTargetVelocity(joint2,5)

		else:
			if dist1 < 0.3 and dist2 < 0.3 and dist3 < 0.3	and dist2 !=0 and dist3 !=0:
				sim.setJointTargetVelocity(joint1,0)
				sim.setJointTargetVelocity(joint2,0)
				Stop = True
			elif dist1< d+1 :

				sim.setJointTargetVelocity(joint1,0)
				sim.setJointTargetVelocity(joint2,0)
				
				t3=2
				t2=5
				if dist2 == 0:
					while (dist3 <= t2) or (t3 == 2):
						t2 = detect_distance_sensor_3(sim)
						sim.setJointTargetVelocity(joint1,speed)
						sim.setJointTargetVelocity(joint2,-speed)
						dist3 = detect_distance_sensor_3(sim)
						if dist3<=t2:
							t3=3
	


				else:
					while (dist2 <= t2) or (t3 == 2):
						t2 = detect_distance_sensor_2(sim)
						sim.setJointTargetVelocity(joint1,-speed)
						sim.setJointTargetVelocity(joint2,speed)
						dist2 = detect_distance_sensor_2(sim)
						if dist2<=t2:
							t3=3
				

	##################################################

def detect_distance_sensor_1(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_1'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_1 = detect_distance_sensor_1(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	dist_1=sim.getObjectHandle('distance_sensor_1')

	data=  sim.readProximitySensor(dist_1)
	if isinstance(data,int):
		distance = data
	else:
		distance = data[1]


	##################################################
	return distance

def detect_distance_sensor_2(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	dist_2=sim.getObjectHandle('distance_sensor_2')
	data=  sim.readProximitySensor(dist_2)
	if isinstance(data,int):
		distance = data
	else:
		distance = data[1]
	
	##################################################
	return distance



def detect_distance_sensor_3(sim):
	"""
	Purpose:
	---
	Returns the distance of obstacle detected by proximity sensor named 'distance_sensor_2'

	Input Arguments:
	---
	`sim`    :   [ object ]
		ZeroMQ RemoteAPI object

	Returns:
	---
	distance  :  [ float ]
	    distance of obstacle from sensor

	Example call:
	---
	distance_2 = detect_distance_sensor_2(sim)
	"""
	distance = None
	##############  ADD YOUR CODE HERE  ##############
	dist_3=sim.getObjectHandle('distance_sensor_3')
	data=  sim.readProximitySensor(dist_3)
	if isinstance(data,int):
		distance = data
	else:
		distance = data[1]
	
	##################################################
	return distance

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
			control_logic(sim)
			time.sleep(5)

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