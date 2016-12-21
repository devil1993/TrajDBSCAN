#stats_TrajDBSCAN.py
import sys
from TrajDBSCAN import *

shared_stops = sys.argv[1]
ground_truth = sys.argv[2]
accepted_distance = int(sys.argv[3])

file = open(shared_stops,"r")
shared_stops_lines = file.read().split('\n')
file.close()

file = open(ground_truth,"r")
ground_truth_lines = file.read().split('\n')
file.close()

true_positive = []
false_positive = []
false_negative = []

shared_stops_points = getPoints(shared_stops_lines)
ground_truth_points = getPoints(ground_truth_lines)

for shared_stop_point in shared_stops_points:
	print "OK"
	is_true_positive = False
	for ground_truth_point in ground_truth_points:
		print "Fishy"
		dist = get_spherical_distance(shared_stop_point[0],ground_truth_point[0],shared_stop_point[1],ground_truth_point[1])
		print shared_stop_point,ground_truth_point,dist
		if dist<accepted_distance:
			is_true_positive = True
			break
	if is_true_positive:
		true_positive += [shared_stop_point]
	else:
		false_positive += [shared_stop_point]

print "False negative calculation"

for ground_truth_point in ground_truth_points:
	is_false_negative = True
	for shared_stop_point in shared_stops_points:
		dist = get_spherical_distance(shared_stop_point[0],ground_truth_point[0],shared_stop_point[1],ground_truth_point[1])
		print shared_stop_point,ground_truth_point,dist
		if dist<accepted_distance:
			is_false_negative = False
			break
	if is_false_negative:
		false_negative += [ground_truth_point]

print "True Positive: ",len(true_positive)
print "False Positive: ",len(false_positive)
print "False Negative: ",len(false_negative)

file = open(ground_truth+"_true_positive","w")
fileWrite(true_positive,file)
file.close()
file = open(ground_truth+"_false_positive","w")
fileWrite(false_positive,file)
file.close()
file = open(ground_truth+"_false_negative","w")
fileWrite(false_negative,file)
file.close()
