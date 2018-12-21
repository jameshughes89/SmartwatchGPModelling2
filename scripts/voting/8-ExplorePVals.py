'''
Generates a table showing the accuracies when looking at time points vs voters. Shows p-values too. 

TOP

'''

import csv
import matplotlib as mpl
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import scipy.stats 


mpl.style.use('classic')
DATA_PATH = './accuracyMatrices/'


tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
#times = ['', '10s', '20s']
times = ['']
#times = [sys.argv[1]]

NUM_VOTERS_START = 1
NUM_VOTERS_STOP = 10

GROUP_SIZE = 50
MAX_GROUP_SIZE = 120


def loadData(fileName):
	# Load the data into a numpy array of floats
	data = np.array(list(csv.reader(open(DATA_PATH + fileName,'r')))).astype(float)
	return data

def turnDataToDicts(fNameStart):
	table = {}	# Will hold the table for the time
	for gs in range(5, MAX_GROUP_SIZE + 1, 5):

		size = {}	# Will hold the rows (acc for each number of voters)
		for voters in range(NUM_VOTERS_START, NUM_VOTERS_STOP + 1):


			# Load up the small acc mats
			fName = fNameStart + str(voters) + '_' + str(gs) + '_' + time + '.csv'
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
	return table

def generatePValueMatrix(data1, d1_size, data2, d2_size):
	# I think there is a *faster* way to do this with numpy function
	# But I will keep it more clear doing it the ol' fashioned wya 
	matrix = np.zeros((len(data1[d1_size]), len(data2[d2_size])))

	for i, d1 in enumerate(data1[d1_size]):
		for j, d2 in enumerate(data2[d2_size]):
			matrix[i,j] = scipy.stats.wilcoxon(data1[d1_size][d1], data2[d2_size][d2])[1]	# [1] gets us the p-value ([0] is the T --- The sum of the ranks of the differences above or below zero, whichever is smaller.)
	
	return matrix



# Create a plot for each time
for time in times:
	
	
	topData = turnDataToDicts('1-AccMat-Small-TOP_')	# This is ugly hack
	randData = turnDataToDicts('2-AccMat-Small-RAND_')
	mixData = turnDataToDicts('3-AccMat-Small-MIX_')

	matrix = generatePValueMatrix(randData, 50, topData, 50)
	plt.matshow(matrix)
	plt.colorbar(label='p-value')

	# Labelling 
	plt.title('Probability Value Matrix\nComparing Accuracies')
	plt.xlabel('Top')
	plt.xticks(range(0,10), range(1,10 + 1,1))
	plt.ylabel('Random')
	plt.yticks(range(0,10), range(1,10 + 1,1))

	# Add text to matrix
	for i, row in enumerate(matrix):
		for j, d in enumerate(row):
			if np.isnan(d):
				continue
			if d > 0.05:
				plt.text(j-.4, i+.2, round(d,3), fontsize=8)
			else:
				plt.text(j-.4, i+.2, round(d,3), fontsize=8, color='r')

	plt.show()
	
		 
















			
