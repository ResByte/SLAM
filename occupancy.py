import random 
from math import *
import sys
import matplotlib.pyplot as plt

import numpy as np


"""
	Define a robot class.
"""


class robot:
	def __init__(self):
		self.x = random.random()*world_size
		self.y = random.random()*world_size
		self.orientation = random.random()*1.0*pi
		self.forward_noise = 0.0
		self.turn_noise = 0.0
		self.sense_noise= 0.0

	def set(self,new_X,new_Y,new_PHI):
		if  new_X>= world_size:
			print new_X
			raise ValueError, 'X coordinate is out of range'
		if  new_Y >= world_size:
			raise ValueError, 'Y coordinate out of bound'
		if new_PHI < -pi or new_PHI >= pi:
			raise ValueError, 'orientation is out of bound'
		self.x = float(new_X) + (world_size/2.0)
		self.y = float(new_Y) + (world_size/2.0)
		self.orientation= float(new_PHI)
	
	def set_noise(self,new_f_noise,new_t_noise, new_s_noise):
		self.turn_noise = float(new_t_noise)
		self.sense_noise = float(new_s_noise)
		self.forward_noise = float(new_f_noise)

	def sense(self):
		Z = []
		for i in range(len(landmarks)):
			dist = landmarks[i]
			dist += random.gauss(0.0,self.sense_noise)
			Z.append(dist)
		return Z

	def move(self, turn, forward):
		if forward < 0 :
			raise ValueError, 'robot cannot move backwards'
		orientation = self.orientation+float(turn) + random.gauss(0.0, self.turn_noise)
		orientation %= 2*pi
		dist = float(forward) + random.gauss(0.0, self.forward_noise)
		x = self.x + (cos(orientation)*dist)
		y = self.y + (sin(orientation)*dist)
		x%= world_size
		y%= world_size
		res = robot()
		res.set(x,y,orientation)
		res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
		return res

	def Gaussian(self, mu, sigma, x):
		return exp(-((mu-x)**2)/(sigma**2)/2.0)/sqrt(2.0*pi*(sigma**2))

	def measurement_prob(self, measurement):
		prob = 1.0
		for i in range(len(landmarks)):
			dist = sqrt((self.x - landmarks[i][0])**2 + (self.y- landmarks[i][1])**2)
			prob +=self.Gaussian(dist, self.sense_noise, measurement[i])
		return prob

	def __repr__(self):
		return '[x = %.6s y = %.6s orient=%.6s]' %(str(self.x),str(self.y),str(self.orientation))


"""
	Read Odometry data from kthdata/dataset2/fused.dat 
"""

def readOdo():
	odo=[]

	with open(sys.argv[1],'r') as odo_file:
		print "-> reading odometry file"
		for line in odo_file:
			odo.append(line.strip().split())
	return odo	

def readLaser():
	laser=[]
	with open(sys.argv[2],'r') as laser_file:
		print "-> reading laser data"
		for line in laser_file:
			laser.append(line.strip().split())
	return laser


# create world

world_size = 300
createWorld = np.zeros([world_size,world_size])
# initialize robot
myrobot = robot()
#print odo_data
x_co=[]

# get odometry data from file
odo_data = readOdo()
# get laser data from file
laser_data = readLaser()

for i in odo_data:
	x_co.append(float(i[1]))

x=[]
y=[]
theta = []
n= 0
for i in odo_data:
	
	angle = float(i[4])
	newx= float(i[1])
	newy= float(i[2])
	covariance=[]
	covariance.append([i[7], i[8],i[9]])
	covariance.append([i[10],i[11],i[12]])
	covariance.append([i[13],i[14],i[15]])
	myrobot.set(newx,newy,angle)
	#myrobot.set_noise()	
	x.append(myrobot.x)
	y.append(myrobot.y)
	
	# get current laser array
	if n< len(laser_data):
		laser_array=[]
		for idx in range(len(laser_data[n])):
			#print idx
			if idx !=0:
				laser_array.append(float(laser_data[n][idx])/1000.0)
	
	for i in range(len(laser_array)):
		if i <=180 and laser_array[i]<=80.0:
			#print laser_array		
			x_lm = float(laser_array[i])*np.cos(float(i) + float(myrobot.orientation))
			y_lm = float(laser_array[i])*np.sin(float(i) + float(myrobot.orientation))
			x_world = int(round(myrobot.x+x_lm))
			y_world = int(round(myrobot.y+y_lm))
			if x_world >= world_size:
				x_world = world_size-1
			if y_world >= world_size:
				y_world = world_size-1
			#print x_world, y_world	
			# upadate map
			ISM = 0.0
			prior = 0.5
			if laser_array[i]<=2.0:
				ISM = 1.0
			if 2.0< laser_array[i]<=50.0:
				ISM = 0.5
			if laser_array[i]>50.0:
				ISM = 0.0
		
			createWorld[x_world][y_world]=createWorld[x_world][y_world] + ISM 		

#	print laser_array
	createWorld[round(myrobot.x)][round(myrobot.y)]=1.0
	theta.append(myrobot.orientation)
	n+=1

#	print myrobot

plt.imshow(createWorld)
plt.show()



	
