import random 
from math import *
import sys
import matplotlib.pyplot as plt

import numpy as np


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
			dist = sqrt((self.x -landmarks[i][0])**2 + (self.y - landmarks[i][1])**2)
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


world_size = 100
createWorld = np.zeros([world_size*2,world_size*2])
myrobot = robot()
odo_data=[]
with open(sys.argv[1],'r') as odo_file:
	print "-> reading laser file"
	for line in odo_file:
		odo_data.append(line.strip().split())
#print odo_data
x_co=[]
for i in odo_data:
	x_co.append(float(i[1]))

x=[]
y=[]
theta = []
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
	
	createWorld[round(myrobot.x)][round(myrobot.y)]=1
	theta.append(myrobot.orientation)

#	print myrobot

plt.imshow(createWorld)
plt.show()



	
