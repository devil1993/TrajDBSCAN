import os
import sys
from math import *
import math
import numpy as np
from scipy.optimize import brentq

fileNames = []
eps = 20
minTime = 3
route = ""
#taking default radius as 15 meters
default_radius = 0.000135

def initialize_name(files):
	global fileNames,route
	fileNames += files
	try:
		route = sys.argv[1]
	except:
		print "Route not provided, all files considered to be in working directory."

def initialize(dist,time):
	global eps,minTime
	eps = dist
	minTime = time

def get_spherical_distance(lat1,lat2,long1,long2):
        """
        Get spherical distance any two points given their co-ordinates (latitude, longitude)
        """
        q=radians(lat2-lat1)
        r=radians(long2-long1)
        lat2r=radians(lat2)
        lat1r=radians(lat1)
        a=sin(q/2)*sin(q/2)+cos(lat1r)*cos(lat2r)*sin(r/2)*sin(r/2)
        c=2*atan2(sqrt(a),sqrt(1-a))
        R=6371*1000
        d=R*c
        return d
def eps_linear_neighbours(point,pointSet):
	N = []
	for pt in pointSet:
		#if pointSet.index(point)>pointSet.index(pt):
			#continue
		#print (pt[0] - point[0]),(pt[1] - point[1])
		
		'''
		dist = math.pow(10000*(pt[1] - point[1]),2.0) + math.pow(10000*(pt[0] - point[0]),2.0)
		dist = math.sqrt(dist)
		dist_n = dist/10000
		#file.write(str(dist_n)+'\n')
		'''
		dist = get_spherical_distance(pt[0],point[0],pt[1],point[1])
		if dist<eps:
			N.insert(len(N),pt)
	return N

def fileWrite(points,file):
	for point in points:
		for item in point:
			file.write(str(item)+",")
		file.write("\n")

def duration(point, neighbours):
	early = point[2]
	late = point[2]
	for neighbour in neighbours:
		#print time, (neighbour[2]- time)
		if (neighbour[2]>late):
			late = neighbour[2]
		if(neighbour[2]<early):
			early = neighbour[2]
	#print duration
	return (late- early)

def union(list1,list2):
	res = list1
	for i in list2:
		if i not in res:
			res.append(i)
	return res
'''
def getMean(points):
	total_lat= 0
	total_long = 0
	for point in points:
		total_long += point[1]
		total_lat += point[0]
	length = len(points)
	mean_lat = total_lat/length
	mean_long = total_long/length
	''
	THIS CALCULATION IS IGNORED AS WE ARE TAKING A CONSTANT RADIUS OF 15 METERS FOR NOW

	total_distance = 0
	for point in points:
		total_distance += math.sqrt(math.pow(mean_lat-point[0],2)+math.pow(mean_long-point[1],2))
	mean_distance = total_distance/length
	''
	return (mean_lat,mean_long,0.000135)
'''
def createSlowPointFiles():
	print "Creating slow point file..."
	for fileName in fileNames:
		outputFile = route+"slow_" + fileName 
		#print fileName
		file = open(route+fileName,"r")
		lines = file.read().split('\n')
		file.close()

		file = open(outputFile,"w")

		pointSet = []

		for line in lines:
		        components = line.split(',')
		        try:
		                point_x = float(components[0])
		                point_y = float(components[1])
		                timeunits = components[2].split(':')
		                point_t = ((int(timeunits[0])*60) + int(timeunits[1])) * 60 + int(timeunits[2])
		                #pointSet.insert(len(pointSet), (point_x,point_y,point_t))
		                pointSet += [(point_x,point_y,point_t)]
		        except Exception, e:
		                #print e
		                pass

		finalPoints = pointSet[:]

		for x in xrange(1,len(pointSet)-2):
			#for us, we consider distance 1 meter between consecutive point as slow. 
		        if get_spherical_distance(pointSet[x][0],pointSet[x+1][0],pointSet[x][1],pointSet[x+1][1]) > 1:
		                finalPoints.remove(pointSet[x+1])
		for x in finalPoints:
		        file.write(lines[pointSet.index(x)]+'\n')
		file.close()
		print "Reduced From ",len(lines),"to",len(finalPoints)
		print "Created slow point file" , outputFile

def findPS():
	print "Looking for personalized stops..."
	for fileName in fileNames:
		outputFile = route + "corePoints_" + fileName
		#print fileName
		file = open(route + "slow_"+fileName,"r")
		lines = file.read().split('\n')
		file.close()

		file = open(outputFile,"w")

		pointSet = []

		for line in lines:
		        components = line.split(',')
		        try:
		                point_x = float(components[0])
		                point_y = float(components[1])
		                timeunits = components[2].split(':')
		                point_t = ((int(timeunits[0])*60) + int(timeunits[1])) * 60 + int(timeunits[2])
		                #pointSet.insert(len(pointSet), (point_x,point_y,point_t))
		                pointSet += [(point_x,point_y,point_t)]
		        except Exception, e:
		                #print e
		                pass
		pts = pointSet[:]

		ps = []
		for point in pointSet:
			print point
			if(point not in pts):
				continue
			pts.remove(point)
			#print len(pts), len(pointSet)
			N = eps_linear_neighbours(point,pointSet)
			#fileWrite(N)	
			if duration(point, N) > minTime:
				C = [point]
				for neighbour in N:
					#print "Neighbour ", neighbour
					if neighbour in pts:
						C = union(C,[neighbour])
						#region testing this part
						#pts.remove(neighbour)
						#end region
						N1 = eps_linear_neighbours(neighbour,pointSet)
						if duration(neighbour,N1) > minTime:
							N = union(N,N1)
				ps.insert(len(ps),C)

		stops = []
		for stop in ps:
			mean_stop = getMean(stop)
			stops.append(mean_stop)

		fileWrite(stops,file)

		file.close()
		print len(ps), " stops found"
		print "Created PS file...",outputFile

def clusterPS():
	print "Creating cluster..."
	for fileName in fileNames:
		outputFile = route + "clusters_" + fileName
		#print fileName
		file = open(route + "corePoints_"+fileName,"r")
		lines = file.read().split('\n')
		file.close()

		file = open(outputFile,"w")

		pointSet = []

		for line in lines:
			components = line.split(',')
			try:
				point_x = float(components[0])
				point_y = float(components[1])
				pointSet += [(point_x,point_y)]
			except Exception, e:
				#print e
				pass
		temp = pointSet[:]
		clusters=[]
		for point in temp:
			if point not in pointSet:
				continue
			N = eps_linear_neighbours(point,pointSet)
			midPoint = getMean(N+[point])
			clusters.append(midPoint)
			for neighbour in N:
				pointSet.remove(neighbour)

		fileWrite(clusters,file)
		print "clusters: ",len(clusters)
		print "Created cluster file", outputFile

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
'''
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
'''
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

def getPoints(lines):
	pointSet = []
	for line in lines:
	        components = line.split(',')
	        try:
	                point_x = float(components[0])
	                point_y = float(components[1])
	                radius = 0
	                if len(components) >2:
	                	radius = float(components[2])
	                #radius = default_radius
	                pointSet += [(point_x,point_y,radius)]
	        except Exception, e:
	                #print e
	                pass
	return pointSet

def createSharedStops():
	delta = 0.0
	#to get some result
	multiplier = 1

	route_name = ""
	try:
		route_name= sys.argv[2]
	except Exception, e:
		print "Routename not provided, shared stops will be given in a file named \'shared_stops\'"
	fileName = route + "all_personal_stops"
	os.system("cat " + route.replace(" ","\ ") + "clusters_* > " + fileName.replace(" ","\ "))
	outputFile = route + "shared_stops_" + route_name
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
'''
createSharedStops()
#Region main execution
initialize()
createSlowPointFiles()
findPS()
clusterPS()
'''
