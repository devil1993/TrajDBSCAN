import os
import sys
from TrajDBSCAN import *

with open('config.txt','r') as inf:
    config = eval(inf.read())

eps = int(config["eps"])
min_time = int(config["mintime"])

#print eps, min_time

for file in config["filenames"]:
	#print file
	#continue
	newpid = os.fork()
	if newpid==0:
		initialize(eps,min_time)
		initialize_name([file])
		createSlowPointFiles()
		findPS()
		clusterPS()
		createSharedStops()
		os._exit(0)
	else:
		print "Process",newpid,"working on",file
