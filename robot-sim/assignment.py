from __future__ import print_function

import time
from sr.robot import *

import numpy as np


offset_array = []
""" array = Contains offset values of the taken tokens"""

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
       

def find_token_silver():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	size (float): size of the token 
	offset (int): number of the token
    """   
    dist = 100
    offset = 100
    size = 100
    for token in R.see():	
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
            dist = token.dist
            offset = token.info.offset #taking the offset value of the most close token
            size = token.info.size #taking the size of the token
	    rot_y = token.rot_y
    if dist == 100:
	return -1, -1, size, offset
    else:
	return dist, rot_y, size, offset	
   	
def find_token_gold():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	size (float): size of the token 
	offset (int): number of the token
    """
    dist = 100
    offset = 100
    size = 100
    for token in R.see():	
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            dist = token.dist
            size = token.info.size #taking the size of the token
            offset = token.info.offset #taking the offset value of the most close token
	    rot_y = token.rot_y
    if dist == 100:
	return -1, -1, size, offset
    else:
	return dist, rot_y, size, offset	


def offset_append(offset):
	"""
	Function to make an array with the offset numbers of the paired tokens
	
	Input: offset (int): takes offset value of the token using the functions find_token_silver() or find_token_gold()
	
	Return:
	offset_array (array): appends the offsets when going to the chosen token (-1 if the chosen token is already paired)
	"""
	
	if offset not in offset_array: #if offset_array does not contain the new offset that the robot found
		offset_array.append(offset) #adds it into the array
		return offset_array
	else: #if offset_array contains the new offset that the robot found
		print("Same token") 
		return -1	
 		
def go_silver():
	"""
	Function in order to find and go to the silver token 
	"""        
	dist, rot, size, offset = find_token_silver() #calls find function for silver	
	
	if dist == -1:
		print("I don't see any silver token")
		turn(10, 0.5)		
	elif dist > d_th:	
		if -a_th <= rot <= a_th: # if the robot is well aligned with the token, we go forward
			if offset not in offset_array: #checks if it is a new token or not
				print("Ah, I see silver token here we are!.")
				drive(50, 0.5)
			else: #if it is same it turns a bit and then finds a new token
				print("Checking token")
				turn(40, 0.5)						
		elif rot < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot > a_th:
			print("Right a bit...")
			turn(+2, 0.5)	
	elif dist <= d_th: # if the distance between tokens that will be paired is less than the threshold
		offset_append(offset)	
		print("Found it")
		R.grab()
		print("Gotcha!")
		
def go_golden():
	"""
	Function in order to find and go to the golden token 
	""" 
	dist, rot, size, offset = find_token_gold()

	if dist == -1:
		print("I don't see any golden token")
		turn(10, 0.5)
	elif dist > size + d_th:	
		if -a_th<= rot <= a_th: # if the robot is well aligned with the token, we go forward
			if offset not in offset_array: #checks if it is a new token or not
				see() #calls the function see() in order not to drag along a silver token
				print("Ah, I see golden token here we are!.")
				drive(50 ,0.5)
			else: #if it is same it turns a bit and then finds a new token
				print("Checking token")
				turn(40, 0.5)						
		elif rot < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot > a_th:
			print("Right a bit...")
			turn(+2, 0.5)
	elif dist <= size + d_th: # if the distance between tokens that will be paired is less than the threshold
		offset_append(offset)
		print("Found it")			
		R.release()
		print("Releasing!")
		drive(-30, 1)
		turn(20, 1)


def see():

	"""
	Function not to drag along a silver token
	
	"""
	markers = R.see() #checks all markers that the robot can see
	rot_s = []
	dist_s = []
	for m in markers: #finds the distance and rot_y of silver tokens
		if m.info.marker_type in (MARKER_TOKEN_SILVER):
			rot_s.append(m.rot_y)

	rot_s = np.array(rot_s)	#makes an array with the rot angles
	
	"""
	Turns a bit in order to avoid collision (another silver token)
	abs(t) > 1e-5: rot_s can contain the tokens angle that it holds so,
	there is a very little angle
	the other condition is for the silver token that can be crashed if the robot does not turn a bit
	"""
	if any(abs(t) > 1e-5 and abs(t) < 20.0 for t in rot_s):
		print("Turn left a bit...")
		turn(-20,0.5) 	
		drive(40,0.5)
		turn(20,0.5)		

while 1:
	if len(offset_array) != 12: #takes length of offset_array, it finishes when it paired all tokens
		if len(offset_array) % 2 == 0:
			go_silver()
		else:
			go_golden()
		
	else: #it prints two sentences indicating that it finishes the task
		print("all tokens are in pairs")
		print("mission completed")
		break		
		
		
		
