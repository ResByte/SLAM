#!/usr/bin/env python

"""This code is a Loop Closure Technique for Topological SLAM.

"""


import cv2
import cv2.cv as cv
import numpy as np
from scipy.cluster.vq import vq, kmeans2, whiten
import matplotlib.pyplot as plt
import sys
from scipy.spatial.distance import euclidean,correlation
import timeit
import heapq
import itertools
import operator

start = timeit.default_timer()


class Node: 
  def __init__(self, hist=None, desc=None,number =None, next=None): 
    self.hist = hist
    self.pool =[desc] 
    self.number =number
    self.next  = next 

  def __str__(self): 
    return str(self.cargo,self.pool) 

def surf_img(img1):
	#Calculate surf desciptors, and apply Kmeans algo to create clusters
	surf = cv2.SURF()
	surf.extended = True
	#kp = surf.detect(img1)
	kp,descript = surf.compute(img1)
	descriptors = np.asarray(des)		
	centroid,label = kmeans2(descriptors,cluster_n,iter=10,thresh=1e-05, minit='random', missing='warn')
	return descript,centroid,label,kp



def create_hist(labels):
	histogram = np.zeros(cluster_n)
	for i in labels:
		histogram[i-1]+=1.0
	sum = reduce(lambda x,y:x+y, histogram)
    return [ x/(sum) for x in histogram]

def hellinger(list1,list2):
    return euclidean(np.sqrt(list1), np.sqrt(list2))/np.sqrt(2) 
		
def percentageMatch(set1,set2):
	# cardinality of a set is the measure of number of elements in the set
	len_intersect =  len(np.array([x for x in set(tuple(x) for x in set2) & set(tuple(x) for x in set1)]))
	len_img = len(set1)
	return (float(len_intersect)*100.0)/float(len_img)
	
	


def detectLoopClosure(hist1,desc1):
	#selectBest(findLoopCandidates(img))
	#to find a loop closure candidate : Global histogram Match
	distance={}
	percentMatch={}
	if len(map)>1:
		for i in map:
			hist2=i.hist
			number=i.number
			distance[number] = hellinger(hist1,hist2)
		sort= sorted(distance.items(), key=lambda x: x[1],reverse=False)
		topR = itertools.islice(sort.iteritems(), R)
		
		#direct feature Matching 	
		for i in list(topR):
			for element in map:
				if i[0]==element.number:
					desc2=element.pool
					percentMatch[number]=percentageMatch(desc1,desc2)
	
		sort_percent= sorted(percentMatch.items(), key=lambda x:x[1],reverse=True)
		key,value = sort_percent.popitem()
		if value >= threshold:
			return key
		
			

def createNode(img):
	desc,cent,lab,keyp = surf_img(img)
	# for these cluster centers create an histogram 
	#by counting number of descriptors in each bin(cluster center) returned from kmeans
	histo = create_hist(cent,lab)
	return node(histo,desc)
	
	

if __name__ == "__main__":
	#initialize variables
	R=5 #Number of nodes to undergo second stage of varification after global histogram matching
	k=1
	cluster_n =10
	number=0
	map=[]
	for i in range(2):
		with open(sys.argv[1],"r") as rgb_file:
			for line in rgb_file:
				a=line.strip().split()
				if a[0]=="#":
					pass
				else:
					if i !=1:
						
						# Sample with uniform sampling of every 5th frame in the list
						if k == 20:
							image = cv2.imread(a[1])
							imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
							desc,cent,labls,keyp = surf_img(imgray)
							histo = create_hist(labls)
							# detect for loop closures 
							if detectLoopClusure(hist,desc) != None:
								#TODO: update_node()
							
							else:
								#create a new node
								
								new_node =Node(histo,desc,number)
								map.append(new_node)
								number+=1
								# TODO: update_map()
							k=1
						else:
							k+=1



stop = timeit.default_timer()
print stop - start 	
