# TrajDBSCAN
A simple implementation of TrajDBSCAN algorithm using python.

TrajDBSCAN algorithm(https://infoscience.epfl.ch/record/175473/files/main.pdf) is implemented on GPS data using python to extract bus stops.

Instructions:

1.

To execute the algorithm on gps trails, update the config.txt file.

Add the file names in the 'filenames' list in the config file.Only list the file name, not the total path. The files should be in same path.
The input files should be comma seperated with following data:

point lat, point long, timestamp in HH:MM:SS

Set eps in meters.

Set mintime in seconds.

2.

Execute the launcher.py file to run the algorithm. It takes 2 command line parameters, first being the directory of the input files and second being the name of the route of trajectory(ex: CityCenter1,Station20,Airport2 etc.).
The output of each step is saved in the same directory as the input files.

First the slow points are extracted from the whole trajectory and saved in a file named slow_[input file name for each input trajectory.

Next, core points are extracted which are the personalised stops for this algorithm. These are saved in file named corePoints_[input file name].

Next, from the core points, clusters are calculated and saved in files named clusters_[input file name].

Finally, all clusters are brought together and shared stops are calculated from it. The shared stops are saved in a file named shared_stops_[the name we given as 2nd command line parameter].

3.

Now if we know the ground truths, a statistical study can be made to compute true positive, false positive and false negative points.
To perform it, we need to run the stats_TrajDBSCAN.py file with 3 command line parameters as:

i) 	shared stop file.

ii) 	ground truth file.

iii)	accepted distance in meters.

it creates 3 files each containing the class of stops(true positive, false positive and false negative).

Cheers.
