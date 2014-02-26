#!/usr/bin/env python

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

def surf_img(img):
	
	imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	
	surf = cv2.SURF()
	surf.extended = True
	kp,des = surf.detectAndCompute(imgray,None)
	features = np.asarray(des)		
	centroid,label = kmeans2(features,cluster_n,iter=10,thresh=1e-05, minit='random', missing='warn')
	return features,centroid,label
	

def calc_hist(lab_idx):
	histo=np.zeros(cluster_n)
	for i in lab_idx:
		histo[i]+=1
	return histo

def calc_distance(v1,v2):
	cor=[]	
	#print len(v1),len(v2)
	for vector in range(len(v1)):
		#print v1[vector],v2[vector]
		cor.append(correlation(v1[vector],v2[vector]))
	return sum(cor)

		
	





def useful(x,y):
	if (x>=0.5 and y <=0.4): 
		# get those images where there is a significant difference and also are not effected  by sudden changes like turns.
		return True

if __name__ == "__main__":
	np.set_printoptions(threshold=np.nan)
	cluster_n = 15
	key=[]
	tmp_hist = []
	index={}
	index_tmp={}
	loop_Closures=[]
	k=1
	with open(sys.argv[1],"r") as rgb_file:
		for line in rgb_file:
			a=line.strip().split()
			if a[0]=="#":
				pass
			else:
				image = cv2.imread(a[1])
				imgray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
				des1,centroids,label1 = surf_img(image)	
				hist = cv2.calcHist(imgray,[0],None,[256],[0,256])
				hist1 = calc_hist(label1)
				
				if k==1:
					key = hist
					tmp_hist = hist
					index[k]=a[1]
				#detectLoopClosure				
					
				t_match =cv2.compareHist(tmp_hist,hist,cv.CV_COMP_BHATTACHARYYA)
				match_k =cv2.compareHist(key,hist,cv.CV_COMP_BHATTACHARYYA) 				
				#tmp_hist = hist
				#print match_k,match_t
				if useful(match_k,match_t):
					
					for j,l in index.iteritems():
						im_node = cv2.imread(l)
						#sort the nodes on the basis of hellinger distance
						hist_node = cv2.calcHist(im_node,[0],None,[256],[0,256])
						match_node = cv2.compareHist(hist_node,hist,cv.CV_COMP_BHATTACHARYYA)
						index_tmp[j]=match_node
			
					if k>=10:
						sort_list={}						
						heap =heapq.nlargest(5,(index_tmp.values()))	 
						#print sort				
						#sort= sorted(index_tmp.items(), key=lambda x: x[1],reverse=True) 	
						#print sort[1]
						for heaps in heap:
							for ky,vl in index_tmp.iteritems():
								if vl==heaps:
									sort_list[ky]=vl
						distance ={}						
						for ky,vl in sort_list.iteritems():
							im_surf=cv2.imread(index[ky])
							des2,cent,label2 = surf_img(im_surf)
							distance[ky] =calc_distance(cent,centroids)							
							hist2=calc_hist(label2)
							
							#distance[ky]=euclidean(hist1,hist2)							
							#print match_fn(des2,des1)
						print index[max(distance.iteritems(), key=operator.itemgetter(1))[0]] ,a[1]
					if k != 1:						
						key = hist
						index[k]=a[1]
					
				tmp_hist=hist	
				k=k+1
	
												
stop = timeit.default_timer()
print stop - start 
