#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2014 Abhinav <abhinav@abhinav-Presario-CQ62-Notebook-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def poseToCord(pose):
	x= float(pose[0])*100.0
	y = float(pose[0])*100.0
	# origin is middle of the map 
	zero_error = MAX_SIZE
	poseX = int(round(x/5.0)) +zero_error
	poseY = int(round(y/5.0))  +zero_error
	return poseX,poseY 



def main():
	# initialize MAP structure 
	fused_data=[]
	laser_data=[]
	odom=[]
	sonar=[]
	flaser=[]
	# each cell in map represent 5 cm 
	
	map_ex= [[0.  for x in range(MAX_SIZE*3)] for x in range(MAX_SIZE*3)]
	print np.shape(map_ex)
	# Read the txt files
	with open(sys.argv[1],"r") as data_file:
		print "->reading files"
		for line in data_file:
			a=line.strip().split()
			if a[0]== '#':
				pass
			elif a[0]== 'ODOM':
				odom.append(a)
			elif a[0]=='SONAR':
				sonar.append(a)
			elif a[0]=='FLASER':
				flaser.append(a)
	print len(odom)
	
	
	return 0

if __name__ == '__main__':
	MAX_SIZE=1600
	main()

