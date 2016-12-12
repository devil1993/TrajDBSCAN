import math
import os
from math import *

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


eps = 20
minTime = 3

fileName = raw_input('Enter filename: ')
outputFile = raw_input('Enter output file name: ')
#print fileName
file = open(fileName,"r")
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

def eps_linear_neighbours(point):
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

def fileWrite(points):
	for point in points:
		file.write(str(point[0])+","+str(point[1])+'\n')

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

def getMean(points):
	total_lat= 0
	total_ling = 0
	for point in points:
		total_ling += point[1]
		total_lat += point[0]
	length = len(points)
	mean_lat = total_lat/length
	mean_long = total_ling/length
	return (mean_lat,mean_long)

pts = pointSet[:]

ps = []
for point in pointSet:
	print point
	if(point not in pts):
		continue
	pts.remove(point)
	#print len(pts), len(pointSet)
	N = eps_linear_neighbours(point)
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
				N1 = eps_linear_neighbours(neighbour)
				if duration(neighbour,N1) > minTime:
					N = union(N,N1)
		ps.insert(len(ps),C)

stops = []
for stop in ps:
	mean_stop = getMean(stop)
	stops.append(mean_stop)

fileWrite(stops)

file.close()
print len(ps), " stops found"