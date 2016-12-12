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

finalPoints = pointSet[:]

for x in xrange(1,len(pointSet)-2):
        if get_spherical_distance(pointSet[x][0],pointSet[x+1][0],pointSet[x][1],pointSet[x+1][1]) > 1:
                finalPoints.remove(pointSet[x+1])
for x in finalPoints:
        file.write(lines[pointSet.index(x)]+'\n')
file.close()

