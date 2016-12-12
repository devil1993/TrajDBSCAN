import os
import numpy as np
from scipy.optimize import brentq
import math

#taking default radius as 15 meters
default_radius = 0.000135

def intersectionArea(d, R, r):
    """Return the area of intersection of two circles.

    The circles have radii R and r, and their centres are separated by d.

    """
    #print d,r,R
    if d <= abs(R-r):
        # One circle is entirely enclosed in the other.
        return np.pi * min(R, r)**2
    if d >= r + R:
        # The circles don't overlap at all.
        return 0

    r2, R2, d2 = r**2, R**2, d**2
    alpha = np.arccos((d2 + r2 - R2) / (2*d*r))
    beta = np.arccos((d2 + R2 - r2) / (2*d*R))
    #print alpha,beta
    #print r2*alpha, R2*beta, 0.5*r2*np.sin(2*alpha), 0.5*R2*np.sin(2*beta)
    return ( r2 * alpha + R2 * beta -
             0.5 * (r2 * np.sin(2*alpha) + R2 * np.sin(2*beta))
           )

def neighbouringValue(point, neighbour, multiplier):
	distance = math.sqrt( (point[0]-neighbour[0])**2 +
						  (point[1]-neighbour[1])**2
						)
	area1 = np.pi*(point[2]*multiplier)**2
	area2 = np.pi*(neighbour[2]*multiplier)**2

	intersection_area = intersectionArea(distance,point[2]*multiplier,neighbour[2]*multiplier)

	union_area = area1 + area2 - intersection_area
	if union_area <= 0:
		return 0
	return (intersection_area/union_area)

def getOverlappingNeighbours(point,delta,pointSet,multiplier):
	N = []
	for possibleNeighbour in pointSet:
		if neighbouringValue(point,possibleNeighbour,multiplier) > delta:
			N.append(possibleNeighbour)
	return N

def fileWrite(points,file):
	for point in points:
		for item in point:
			file.write(str(item)+",")
		file.write("\n")

def union(list1,list2):
	res = list1
	for i in list2:
		if i not in res:
			res.append(i)
	return res

def getMean(points):
	total_lat= 0
	total_long = 0
	for point in points:
		total_long += point[1]
		total_lat += point[0]
	length = len(points)
	mean_lat = total_lat/length
	mean_long = total_long/length
	total_distance = 0
	for point in points:
		total_distance += math.sqrt(math.pow(mean_lat-point[0],2)+math.pow(mean_long-point[1],2))
	mean_distance = total_distance/length
	return (mean_lat,mean_long,mean_distance)

def createSharedStops():
	delta = 0.0
	#to get some result
	multiplier = 1
	fileName = "all_personal_stops"
	os.system("cat clusters_* > " + fileName)
	outputFile = "shared_stops" 
	#print fileName
	file = open(fileName,"r")
	lines = file.read().split('\n')
	file.close()

	file = open(outputFile,"w")
	global default_radius
	pointSet = []
	shared_stops = []
	for line in lines:
	        components = line.split(',')
	        try:
	                point_x = float(components[0])
	                point_y = float(components[1])
	                #radius = float(components[2])
	                radius = default_radius
	                pointSet += [(point_x,point_y,radius)]
	        except Exception, e:
	                #print e
	                pass

	finalPoints = pointSet[:]

	for point in pointSet:
		print point
		if point not in finalPoints:
			continue
		finalPoints.remove(point)
		N = getOverlappingNeighbours(point, delta,pointSet,multiplier)
		for n in N:
			if n in finalPoints:
				N1 = getOverlappingNeighbours(n,delta, pointSet,multiplier)
				N = union(N,N1)
		if len(N)>1:
			print "Found shared stop with",len(N), "stops"
			'''
			TODO : convex hull N---> to be implemented by mean as center 
				   and round with radius mean distances
			'''
			mean_stop = getMean(N)
			#not to be done?
			for stop in N:
				if stop in finalPoints:
					finalPoints.remove(stop)
					
			shared_stops.append(mean_stop)
				
	fileWrite(shared_stops,file)
	return shared_stops

createSharedStops()