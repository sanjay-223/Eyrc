'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3D of Pharma Bot (PB) Theme (eYRC 2022-23).
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
# Filename:			socket_client_rgb.py
# Functions:		
# 					[ Comma separated list of functions in this file ]

####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv)                    ##
##############################################################
import socket
import time
import os, sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

def reset():
	Red.ChangeDutyCycle(0)
	Green.ChangeDutyCycle(0)
	Blue.ChangeDutyCycle(0)

##############################################################

def setup_client(host, port):

	"""
	Purpose:
	---
	This function creates a new socket client and then tries
	to connect to a socket server.

	Input Arguments:
	---
	`host` :	[ string ]
			host name or ip address for the server

	`port` : [ string ]
			integer value specifying port name
	Returns:

	`client` : [ socket object ]
			   a new client socket object
	---

	
	Example call:
	---
	client = setup_client(host, port)
	""" 

	client = None

	##################	ADD YOUR CODE HERE	##################
	
	client =  socket.socket()
	client.connect((host,port))

	##########################################################

	return client

def receive_message_via_socket(client):
	"""
	Purpose:
	---
	This function listens for a message from the specified
	socket connection and returns the message when received.

	Input Arguments:
	---
	`client` :	[ socket object ]
			client socket object created by setup_client() function
	Returns:
	---
	`message` : [ string ]
			message received through socket communication
	
	Example call:
	---
	message = receive_message_via_socket(connection)
	"""

	message = None

	##################	ADD YOUR CODE HERE	##################

	message = client.recv(1024).decode()

	##########################################################

	return message

def send_message_via_socket(client, message):
	"""
	Purpose:
	---
	This function sends a message over the specified socket connection

	Input Arguments:
	---
	`client` :	[ socket object ]
			client socket object created by setup_client() function

	`message` : [ string ]
			message sent through socket communication

	Returns:
	---
	None
	
	Example call:
	---
	send_message_via_socket(connection, message)
	"""

	##################	ADD YOUR CODE HERE	##################

	client.send(message.encode())

	##########################################################

def rgb_led_setup(gnd_pin,red_pin,green_pin,blue_pin):
	"""
	Purpose:
	---
	This function configures pins connected to rgb led as output and
	enables PWM on the pins 

	Input Arguments:
	---
	You are free to define input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	rgb_led_setup()
	"""

	##################	ADD YOUR CODE HERE	##################

	GPIO.setup(gnd_pin,GPIO.OUT)
	GPIO.setup(red_pin,GPIO.OUT)
	GPIO.setup(blue_pin,GPIO.OUT)
	GPIO.setup(green_pin,GPIO.OUT)

	GPIO.output(gnd_pin,GPIO.LOW)	

	R = GPIO.PWM(red_pin,100)
	G = GPIO.PWM(green_pin,100)
	B = GPIO.PWM(blue_pin,100)

	R.start(0)
	G.start(0)
	B.start(0)


	return R,G,B
	
	
	##########################################################
	
def rgb_led_set_color(color):
	"""
	Purpose:
	---
	This function takes the color as input and changes the color of rgb led
	connected to Raspberry Pi 

	Input Arguments:
	---

	`color` : [ string ]
			color detected in QR code communicated by server
	
	You are free to define any additional input arguments for this function.

	Returns:
	---
	You are free to define output parameters for this function.
	
	Example call:
	---
	rgb_led_set_color(color)
	"""    

	##################	ADD YOUR CODE HERE	##################
	reset()
	r,g,b = pwm_values[color]
	Red.ChangeDutyCycle(int((r/256)*100))
    Green.ChangeDutyCycle(int((g/256)*100))
    Blue.ChangeDutyCycle(int((b/256)*100))
	
	##########################################################

if __name__ == "__main__":

		host = "192.168.137.1"
		port = 5050

		## 
		redPin = 24
		gndPin = 23
		greenPin = 5
		bluePin = 18

		## PWM values to be set for rgb led to display different colors
		pwm_values = {"Red": (255, 0, 0), "Blue": (0, 0, 255), "Green": (0, 255, 0), "Orange": (255, 35, 0), "Pink": (255, 0, 122), "Sky Blue": (0, 100, 100)}


		## Configure rgb led pins
		Red,Green,Blue = rgb_led_setup(gndPin,redPin,greenPin,bluePin)


		## Set up new socket client and connect to a socket server
		try:
			client = setup_client(host, port)


		except socket.error as error:
			print("Error in setting up server")
			print(error)
			sys.exit()

		## Wait for START command from socket_server_rgb.py
		message = receive_message_via_socket(client)
		if message == "START":
			print("\nTask 3D Part 3 execution started !!")

		while True:
			## Receive message from socket_server_rgb.py
			message = receive_message_via_socket(client)

			## If received message is STOP, break out of loop
			if message == "STOP":
				print("\nTask 3D Part 3 execution stopped !!")
				break
			else:
				print("Color received: " + message)
				rgb_led_set_color(message)