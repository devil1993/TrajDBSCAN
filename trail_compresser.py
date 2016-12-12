fileName = raw_input('Enter filename: ')
file = open(fileName,"r")
lines = file.read().split('\n')
file.close()

outputFile = raw_input('Enter output file name: ')
file = open(outputFile,"w")

for i in xrange(0,len(lines)-1,3):
	file.write(lines[i]+'\n')
file.close()
