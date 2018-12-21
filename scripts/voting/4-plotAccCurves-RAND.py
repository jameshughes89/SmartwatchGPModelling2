'''
Plot the accuracy curves for the RAND data. 
Make a 3D plot to show how the 3 dimensions matter (accuracy vs time points vs # voters


'''

import csv
import numpy as np
import sys

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D



DATA_PATH = './'


tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']
#times = ['']
#times = [sys.argv[1]]


NUM_VOTERS_START = 1
NUM_VOTERS_STOP = 10
MAX_GROUP_SIZE = 120

# For mean set to 0
# For median, set to 2
MEAN_MED = 0

def loadData(fileName):
	# Load the data into a numpy array of floats
	data = np.array(list(csv.reader(open(DATA_PATH + fileName,'r')))).astype(float)
	return data


# Create a plot for each time
for time in times:

	allData = []
	for voters in range(NUM_VOTERS_START, NUM_VOTERS_STOP + 1):

		# The name of the file we're opening. 		
		fName = '2-accCurveNoSameTake-RAND-' + str(voters) + '_' + time + '.csv'
		allData.append(loadData(fName))
	allData = np.array(allData)

	#ad = []
	#for voters in range(0, 10):
	#	for i, g in enumerate(range(5, MAX_GROUP_SIZE +1, 5)):
	#		ad.append([allData[voters][i][MEAN_MED], g, voters])

	#ad = np.array(ad)
	
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	# This is the mesh of data (the top of the curve)
	Z = allData[:,:,MEAN_MED]
	X = np.arange(5, MAX_GROUP_SIZE +1, 5)
	Y = np.arange(1,10 + 1,1)
	X, Y = np.meshgrid(X, Y)

	surface = ax.plot_surface(Y, X, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

	# Customize the z axis.
	ax.set_zlim(0.2, 1.00)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	# Add a color bar which maps values to colors.
	fig.colorbar(surface, aspect=5)	

	# Try drawing some text
	# Shows the 5tp area
	for v in range(10):
		#for i, dp in enumerate(range(5,121,5)):
		ax.text(v, 5, allData[v,0,MEAN_MED], str(round(allData[v,0,MEAN_MED], 3)), 'y', fontsize=7)

	# Shows the 50tp area
	for v in range(10):
		#for i, dp in enumerate(range(5,121,5)):
		ax.text(v, 50, allData[v,9,MEAN_MED], str(round(allData[v,9,MEAN_MED], 3)), 'y', fontsize=7)

	# Shows the 120tp area
	for v in range(10):
		#for i, dp in enumerate(range(5,121,5)):
		ax.text(v, 120, allData[v,23,MEAN_MED], str(round(allData[v,23,MEAN_MED], 3)), 'y', fontsize=7)

	ax.set_xlabel('Voters')
	ax.set_ylabel('Time Points')
	ax.set_zlabel('Accuracy')

	if time == '':
		name = 'all'
	else:
		name = time
	plt.title('Accuracy Curve --- Random: ' + name)
	plt.show()

			
