import random 
from math import *


landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]] 
world_size = 100.0
T = 20


class robot:
	def __init__(self):
		self.x = random.random()*world_size
		self.y = random.random()*world_size
		self.orientation = random.random()*2.0*pi
		self.forward_noise = 0.0
		self.turn_noise = 0.0
		self.sense_noise= 0.0

	def set(self,new_X,new_Y,new_PHI):
		if new_X<0 or  new_X>= world_size:
			raise ValueError, 'X coordinate is out of range'
		if new_Y < 0 or new_Y >= world_size:
			raise ValueError, 'Y coordinate out of bound'
		if new_PHI <0 or new_PHI >= 2*pi:
			raise ValueError, 'orientation is out of bound'
		self.x = float(new_X)
		self.y = float(new_Y)
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




class particle_filter(robot):
	def __init__(self):
		self.p = []
		self.nparticles = 0
	
	def assign(self,n):
		self.nparticles = n
		for i in range(self.nparticles):
			r = robot()
			r.set_noise(0.05,0.05,5.0)
			self.p.append(r)
	
	
	def update(self,dx,dy,mes):
		p2 = []
		for i in range(self.nparticles):
			p2.append(self.p[i].move(dx,dy))
		self.p = p2
		w = []
		for i in range(self.nparticles):
			w.append(self.p[i].measurement_prob(mes))
		p3=[]
		index = int(random.random()*self.nparticles)
		beta = 0.0
		mw = max(w)
		for i in range(self.nparticles):
			beta +=random.random()*2.0*mw
			while beta > w[index]:
				beta -= w[index]
				index = (index +1)%self.nparticles
			p3.append(self.p[index])
		self.p = p3
	def __repr__(self):
		return '[number of particles = %s max = %s]' %(str(self.nparticles),str(max(self.p)))


myrobot = robot()
pf = particle_filter()

pf.assign(1000)
for t in range(T):
	myrobot = myrobot.move(0.1,5.0)
	print 'myrobot',myrobot
	Z= myrobot.sense()	
	pf.update(0.1,5.0,Z)
	print 'pf',pf

	
