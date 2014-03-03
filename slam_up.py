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
  def __init__(self, hist=None, desc=None,number =None): 
    self.hist = hist
    self.pool =[desc] 
    self.number =number

  def __str__(self): 
    return str(self.hist,self.pool,self.number) 

def surf_img(img1):
	print "-> calculating SURF"
	#Calculate surf desciptors, and apply Kmeans algo to create clusters
	surf = cv2.SURF()
	surf.extended = True
	#kp = surf.detect(img1)
	kp,descript = surf.detectAndCompute(img1,None)
	descriptors = np.asarray(descript)		
	centroid,label = kmeans2(descriptors,cluster_n,iter=10,thresh=1e-05, minit='random', missing='warn')
	return descript,centroid,label,kp



def create_hist(labels):
	print "-> calculating histogram"
	histogram = np.zeros(cluster_n)
	for i in labels:
		histogram[i]+=1.0
	sum2 = reduce(lambda x,y:x+y, histogram)
	for i in histogram:
		i = i/sum2
	return histogram

def hellinger(list1,list2):
	print "-> hellinger"
	return euclidean(np.sqrt(list1), np.sqrt(list2))/np.sqrt(2) 
		
def percentageMatch(set1,set2):
	print "->percentage match"
	# cardinality of a set is the measure of number of elements in the set
	# wrong method 
	# TODO: compute SURF correspondances between incoming image and given node
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(set1,set2, l=2)
	len_img = len(set1)
	# Sort them in the order of their distance.
	#matches = sorted(matches, key = lambda x:x.distance)
	good = []
	for m,n in matches:
		if m.distance < 0.75*n.distance:
			good.append([m])	
	#len_intersect =  len(np.array([x for x in set(tuple(x) for x in set2) & set(tuple(x) for x in set1)]))
	len_intersect= len(good)
	len_img = len(set1)
	print "-> return from percent match"
	#print matches
	return (float(len_intersect)*100.0)/float(len_img)
	
	


def detectLoopClosure(hist1,desc1):
	print "-> detect loop closure"
	#selectBest(findLoopCandidates(img))
	#to find a loop closure candidate : Global histogram Match
	distance={}
	percentMatch={}
	# This is a linear search, better to implement a BST or K-d tree.
	
	for i in map:
			hist2=i.hist
			number=i.number
			distance[number] = hellinger(hist1,hist2)
	sort= sorted(distance.items(), key=lambda x: x[1],reverse=False)
	topR = itertools.islice(sort, R)
		
		#direct feature Matching 	
	for i in list(topR):
		for element in map:
			if i[0]==element.number:
				print "-> In percentMatch"
				desc2=element.pool[0]
	#			print desc2.shape
	#			print desc1.shape
				bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

				# Match descriptors.
				matches = bf.match(desc1,desc2)
				len_intersect= len(matches)
				len_img = len(desc1)
				print "-> return from percent match"
				#print matches
				#return (float(len_intersect)*100.0)/float(len_img)
				percentMatch[number]=(float(len_intersect)*100.0)/float(len_img)
	print "-> second step of loop closure"
	#print percentMatch
	sort_percent= sorted(percentMatch.items(), key=lambda x:x[1],reverse=True)
	#print sort_percent
	value = sort_percent[0]
	#print value[1]
	if value[1] >= threshold:
		print "loop closure detected"
		return value[0]
		
			

def createNode(img):
	"""desc,cent,lab,keyp = surf_img(img)
	# for these cluster centers create an histogram 
	#by counting number of descriptors in each bin(cluster center) returned from kmeans
	histo = create_hist(cent,lab)
	return node(histo,desc)"""
	#adjacencyMatrix][]
	


def updateNodeProbabilities(node_num,prev):
	print "update Node Probabilities"
	sum_prior_nodes = sum(node_prior)
	# update P(theta)
	for  i in range(MAX_NODES):
		if i == node_num:
			node_probability_vector[node_num]=(node_prior[node_num]+1.0)/(sum_prior_nodes + 1.0)
		else:
			node_probability_vector[i]=node_prior[i]/(sum_prior_nodes + 1.0)
	
	# This detects how many times a node is found to be loop closure
	for i in range(MAX_NODES):
		if i ==node_num:
			node_prior[node_num]+=1.0
	
	Dt = sum(node_prior)
	if node_num != prev:
		sum_hyper= sum(hyperparameters_rv_prior[node_num])
		for i in range(MAX_NODES):
			if i == prev:
				transition_probability_nodes[prev][node_num]=(hyperparameters_rv_prior[prev][node_num]+1.0)/(sum_hyper+1.0)
			else:
				transition_probability_nodes[i][node_num]=(hyperparameters_rv_prior[i][node_num])/(sum_hyper+1.0)
		for i in range(MAX_NODES):
			if i == prev:
				hyperparameters_rv_prior[prev][node_num]=hyperparameters_rv_prior[prev][node_num]+1.0
	
	
	
			
	#if node_num != dst_node_num:
		##print hyperparametes_rv_prior[node_num]
		#parent_X_sum = sum(hyperparametes_rv_prior[node_num])
		
		#for i in range(MAX_NODES):
			#if i == dst_node_num:
				#transition_probability_nodes[dst_node_num][node_num]=(hyperparametes_rv_prior[dst_node_num][node_num]+1.0)/(parent_X_sum +1.0)
			#else:
				#transition_probability_nodes[i][node_num]=(hyperparametes_rv_prior[i][node_num]+1.0)/(parent_X_sum +1.0)
		
		#for i in range(MAX_NODES):
			#if i==dst_node_num:
				#hyperparametes_rv_prior[dst_node_num][node_num]=(hyperparametes_rv_prior[dst_node_num][node_num]+1.0)
			
	
def update_node(node_id,histo,desc):
	print "-> update node"
	for i in map:
		if i.number==node_id:
			i.pool.append(desc)

def updateTransition(new,last):
	if new!=last:
			adjacencyMatrix[new][last]=1.0			
		
	

if __name__ == "__main__":
	#initialize variables
	np.set_printoptions(threshold=np.nan)
	print "->Initializing Variables"
	first = True
	MAX_NODES=160
	R=5 #Number of nodes to undergo second stage of varification after global histogram matching
	kint=1
	cluster_n =10
	number=0
	loopClosureCount=0
	eachVistedNode=np.zeros(MAX_NODES)
	visitedNode=np.zeros(MAX_NODES)
	node_num=0
	dst_node_num=0
	lastNode =0
	threshold =50.0 
	adjacencyMatrix=np.zeros([MAX_NODES,MAX_NODES])
	transition_probability_nodes=np.zeros((MAX_NODES,MAX_NODES)) # adjacency matrix
	init_node_probabilities=1.0/MAX_NODES
	node_probability_vector=[1.0/MAX_NODES for x in range(MAX_NODES)]  # theta from the paper
	
	node_prior = [0. for x in range(MAX_NODES)] # each element is Di and sum is Dt

	""" 
    // We are assuming the Drichlet prior for n Random variables (X1,X2,......Xn)
    // X1~Drichlet(Alpha1,Alpha2.......) X2~Drichlet(Alpha..)


    // Posterior distribution X1~Drichlet(Alpha1+N1,Alpha2+N2......) and so on.......

    // parameter estimation i.e. updating transition probabilities given its parents
    // theta(i/j) = alpha(i/j)+N(i,j) / aplha + N; """

	X_Rv=[1.0/MAX_NODES for x in range(MAX_NODES)]
	hyperparameters_rv_prior =[X_Rv for x in range(MAX_NODES)]
		
	map=[]
	imgCount= 0
	prevNode=0

	
	with open(sys.argv[1],"r") as rgb_file:
		print "->reading files"
		for line in rgb_file:
			a=line.strip().split()
			if a[0]=="#":
				pass
			else:					
			# Sample with uniform sampling of every 20th frame in the list
				if kint == 10:
					print "->reading images" 
					if first:
						print "->reading first image"
						image = cv2.imread(a[1])
						imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
						imgCount+=1
						dptr,cent,labls,keyp = surf_img(imgray)
						histo = create_hist(labls)
							#adjacencyMatrix[0][0]=1.0
						eachVistedNode[0]=1
						visitedNode[0]=1
						prior=[1.0]
						map.append(Node(histo,dptr,0))
						
						first = False
					else:	
						image = cv2.imread(a[1])
						imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
						imgCount+=1
						dptr,cent,labls,keyp = surf_img(imgray)
						histo = create_hist(labls)
						
						node_key=detectLoopClosure(histo,dptr)
						# detect for loop closures 
						if node_key != None:
							print "->detected loop closure"
							#TODO: update_node()
							updateNodeProbabilities(node_key,prevNode)
							loopClosureCount+=1
							update_node(node_key,histo,dptr)
							prevNode=node_key
						else:
							#create a new node
							print "->creating a new node"
							number+=1
							new_node =Node(histo,dptr,number)
							map.append(new_node)
							updateTransition(new_node.number,prevNode)
							#updateNodeProbabilities(new_node.number,prevNode)
							prevNode = new_node.number
							# TODO: update_map()
					kint=1
				else:
					kint+=1
	print "-> transition probabilities"
	print transition_probability_nodes
	print "-> ajacency matrix"
	print adjacencyMatrix
	



stop = timeit.default_timer()
print stop - start 	
