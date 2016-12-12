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
		pointSet += [(point_x,point_y)]
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

temp = pointSet[:]
clusters=[]
for point in temp:
	if point not in pointSet:
		continue
	clusters.append(point)
	N = eps_linear_neighbours(point)
	for neighbour in N:
		pointSet.remove(neighbour)

fileWrite(clusters)
print len(clusters)
