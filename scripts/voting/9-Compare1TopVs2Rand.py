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

	sameTime = []
	diff1Time = []
	diff2Time = []
	diff3Time = []
	for gs in range(5, MAX_GROUP_SIZE + 1, 5):
		wilcox = scipy.stats.wilcoxon(topData[gs][2], mixData[gs][5])
		sameTime.append(wilcox[1])

		# if we're not at the edge case
		if gs > 5:
			wilcox = scipy.stats.wilcoxon(topData[gs][2], mixData[gs-5][2])
			diff1Time.append(wilcox[1])
		

		# if we're not at the edge case again
		if gs > 10:
			wilcox = scipy.stats.wilcoxon(topData[gs][2], mixData[gs-10][2])
			diff2Time.append(wilcox[1])

		# if we're not at the edge case again
		if gs > 15:
			wilcox = scipy.stats.wilcoxon(topData[gs][2], mixData[gs-15][2])
			diff3Time.append(wilcox[1])


	plt.plot(range(0, len(sameTime)), sameTime, label='Same Time Points')
	plt.fill_between(range(0, len(sameTime)), 0, sameTime)
	plt.plot(range(1, len(sameTime)), diff1Time, label='Less 0.5s')
	plt.fill_between(range(1, len(sameTime)), 0, diff1Time, color='g')
	plt.plot(range(2, len(sameTime)), diff2Time, label='Less 1s')
	plt.fill_between(range(2, len(sameTime)), 0, diff2Time, color='r')
	plt.plot(range(3, len(sameTime)), diff3Time, label='Less 1.5s')
	plt.fill_between(range(3, len(sameTime)), 0, diff3Time, color='c')

	plt.axhline(0.05, color='k', linestyle=':')
	plt.fill_between(range(0, len(sameTime)), 0, [0.05]*len(sameTime), color='grey')
	plt.xticks(range(0,len(sameTime)), range(5, MAX_GROUP_SIZE + 1, 5)) 
	plt.xlabel('Number of Time Points Given to Top Model Classifier')
	plt.xlim((0,len(sameTime)-1))
	plt.ylabel('p-Value Between Top Model With 5 Vote Classifier\nand Random Model With 6 Votes')

	plt.title('Comparing Top Model Classifier\nand Random Model Classifier')
	plt.legend(fontsize=8)
	plt.show()







			
