'''
Generates a table showing the accuracies when looking at time points vs voters. Shows p-values too. 

TOP

'''

import csv
import numpy as np
import scipy.stats 

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
	
	table = {}	# Will hold the table for the time
	for gs in range(5, MAX_GROUP_SIZE + 1, 5):

		size = {}	# Will hold the rows (acc for each number of voters)
		for voters in range(NUM_VOTERS_START, NUM_VOTERS_STOP + 1):


			# Load up the small acc mats
			fName = '3-AccMat-Small-MIX_' + str(voters) + '_' + str(gs) + '_' + time + '.csv'
			smallMat = loadData(fName)

			# Go through the diagonal (kinda, it's not really a diag, more like a staircase)					
			# And record how often it was right
			diagValues = []
		
			# This is ugly, but works...
			# 150 rows, 30 cols remember
			# So we need to look at 5 rows for each col. 
			for i in range(30):
				for j in range(5):
					diagValues.append(smallMat[i*5+j,i])	
			
			# Add the diagonal values to the dict holding the table info
			# This data will be used to generate the table later. 
			# Now we just store all the info 
			size[voters] = diagValues
		table[gs] = size


	print time
	for gs in range(5, MAX_GROUP_SIZE + 1, 5):
		# Build a string for each line
		s = '\hline ' + str(gs) + ' &\t '
		for voters in range(NUM_VOTERS_START, NUM_VOTERS_STOP + 1): 
			s +=  str(round(np.mean(table[gs][voters]), 3)) + '/' 
			s += str(round(np.median(table[gs][voters]), 3))
			s += ' (' + str(round(scipy.stats.mannwhitneyu(table[gs][1], table[gs][voters])[1], 3)) + ')'	# Man whitney U
			if voters < NUM_VOTERS_STOP:
				s += '\t& '
		s += ' \\\\'
		print s

	print '\n\n\n'

	
		 
















			
