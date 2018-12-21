'''
DO NOT NEED ANYMORE. 

Addresses an old problem with the 3-mixed script where it saved the whole mat as the small mat. 

This script opens the large one and creats the small one and saves it. 

'''

import csv
import numpy as np

DATA_PATH = './accuracyMatrices/'


tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']
#times = ['']
#times = [sys.argv[1]]

NUM_VOTERS_START = 1
NUM_VOTERS_STOP = 10

GROUP_SIZE = 50
MAX_GROUP_SIZE = 120


def loadData(fileName):
	# Load the data into a numpy array of floats
	data = np.array(list(csv.reader(open(DATA_PATH + fileName,'r')))).astype(float)
	return data


# Create a plot for each time
for time in times:

	for voters in range(NUM_VOTERS_START, NUM_VOTERS_STOP + 1):
		for gs in range(5, MAX_GROUP_SIZE + 1, 5):

			print time, voters, gs
			fName = '3-AccMat-MIX_' + str(voters) + '_' + str(gs) + '_' + time + '.csv'
			accMat = loadData(fName)	


			# Where we will store the compressed version of the mat
			# This will smush it over the takes
			accMatSmall = []

			# For each row, we'll sum up the accuracies over all takes of the same subject/task
			# Will result in 150 rows, 30 cols. 
			# Note, each row will add up to 1.00 (100%)
			#	Or at least it should... it's possible two models tie, but this would be very very unusual considering floats
			for i in range(0, accMat.shape[0], 1):
				accMatRow = []

				# For each group of 5 (take)
				# Add up the accuracies over the 5
				for j in range(0, accMat.shape[0], 5):
					accMatRow.append(np.sum(accMat[i, j:j+5]))
		
				accMatSmall.append(accMatRow)

			accMatSmall = np.array(accMatSmall)
	
			# Save the small accuracy matrix here
			np.savetxt('./accuracyMatrices/3-AccMat-Small-MIX_' + str(voters) + '_' + str(gs) + '_' + time + '.csv', accMatSmall, delimiter=',') 
