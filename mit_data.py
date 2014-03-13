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
	Read Odometry data from MIT dataset of Infinite Corridor 
"""


def readMitData():
	odom_data=[]
	sonar_data=[]
	flaser_data=[]
	with open(sys.argv[1],'r') as data_file:
		print"-> reading data"
		for line in data_file:
			a = line.strip().split()
			if a[0]=='ODOM':
				odom_data.append(a)
			if a[0]=='SONAR':
				sonar_data.append(a)
			if a[0]=='FLASER':
				flaser_data.append(a)

	return odom_data,sonar_data,flaser_data



		
# create world

world_size = 1300
createWorld = np.zeros([world_size,world_size])
# initialize robot
myrobot = robot()
#print odo_data
x_co=[]

# get odometry data from file
odom, sonar, flaser = readMitData()
# get laser data from file



for i in flaser:
	angle = float(i[184])
	newx = float(i[182])
	newy=float(i[183])
	#print i[184]
	myrobot.set(newx,newy,angle)
	laser_array=[]
	for n in range(180):
		x_lm = float(i[n+2])*cos(float(n) + angle)
		y_lm = float(i[n+2])*sin(float(n)+ angle)
		x_world = round(myrobot.x+x_lm)
		y_world = round(myrobot.y + x_lm)		
#		laser_array.append(float(i[n+2]))
		if x_world >= world_size:
			x_world = world_size-1
		if y_world >= world_size:
			y_world = world_size-1
			#print x_world, y_world	
			# upadate map
		ISM = 0.0
		prior = 0.5
		if i[n+2]<=20.0:
			ISM = 1.0
		if 20.0< i[n+2]<=50.0:
			ISM = 0.5
		if i[n+2]>50.0:
			ISM = 0.0
		
		createWorld[x_world][y_world]=createWorld[x_world][y_world] + ISM + prior 
	#odometry.append(float(i[184]))
	
	#print laser_array

plt.imshow(createWorld,origin='lower')
plt.show()

