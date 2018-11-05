'''
Print out the accuracy matrix for a given GROUP_SIZE. 

Figure out the GROUP_SIZE based on script 6, the one the prints the accuracy curves. In the previous paper (CIBCB 2018) it was 50. 


'''

import csv
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import sklearn.linear_model
import sys



tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
#times = ['']
times = ['', '10s', '20s']
#times = [sys.argv[1]]


# 50, because that's what was in the previous paper, but can be changed
GROUP_SIZE = 100	

# Probably leave them as 0 -- 1
V_MIN = 0.0		
V_MAX = 1.0

def plotMatrices(accMat, AccMatSmall, time, regType):
	pltz = []

	axes = plt.subplot2grid((1,2), (0,0))
	pltz.append(axes)
	img = pltz[0].matshow(accMat, vmin=V_MIN, vmax=V_MAX)

	for i in range(30, 121, 30):
		pltz[0].axvline(i - 0.5, color='k', linewidth=2)
		pltz[0].axhline(i - 0.5, color='k', linewidth=2)

	for i in range(5, 151, 5):
		pltz[0].axvline(i - 0.5, color='k', linewidth=1, linestyle='--')
		pltz[0].axhline(i - 0.5, color='k', linewidth=1, linestyle='--')



	pltz[0].set_title('', fontsize=12)
	pltz[0].set_ylabel('Data',rotation=90)
	pltz[0].set_xlabel('Model')
	pltz[0].set_yticks(range(15,150,30))
	pltz[0].set_yticklabels(tasks, rotation=90)
	pltz[0].set_xticks(range(15,150,30))
	pltz[0].set_xticklabels(tasks, rotation=0)

	divider = make_axes_locatable(axes)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(img, cax = cax)


	axes = plt.subplot2grid((1,2), (0,1))
	pltz.append(axes)
	img = pltz[1].matshow(AccMatSmall, vmin=V_MIN, vmax=V_MAX, aspect='auto')

	for i in range(6, 30, 6):
		pltz[1].axvline(i - 0.5, color='k', linewidth=2)

	for i in range(30, 121, 30):
		pltz[1].axhline(i - 0.5, color='k', linewidth=2)

	for i in range(5, 151, 5):
		pltz[1].axhline(i - 0.5, color='k', linewidth=1, linestyle='--')

	pltz[1].set_title('', fontsize=12)
	#pltz[1].set_ylabel('Data',rotation=90)
	pltz[1].set_xlabel('Model')
	pltz[1].set_yticks(range(15,150,30))
	pltz[1].set_yticklabels(tasks, rotation=90)
	pltz[1].set_xticks(range(2,30,6))
	pltz[1].set_xticklabels(tasks, rotation=0)
	divider = make_axes_locatable(axes)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(img, cax = cax)

	
	# didnt work well with matshow
	plt.suptitle('Confusion Matrix: ' + time + ', ' + regType, fontsize=16)
	plt.show()


def smushMatrix(accMat, regType, time):
	'''
	Function to smush the full accuracy matrix. Should only call this if I need to actually generate it. 
	'''

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
	np.savetxt('./accuracyMatrices/5-AccMatSmall_' + str(GROUP_SIZE) + '_' + time + '_' + regType + '.csv', accMatSmall, delimiter=',')
	return accMatSmall


def printMatrices(regType = 'OLS'):
	for time in times:
		accMat = np.array(list(csv.reader(open('./accuracyMatrices/5-AccMat_' + str(GROUP_SIZE) + '_' + time + '_' + regType + '.csv','r')))).astype(float)
		#accMatSmall = np.array(list(csv.reader(open(DATA_PATH + '5-AccMatSmall_' + str(GROUP_SIZE) + '_' + time + '_' + regType + '.csv','r')))).astype(float)
		accMatSmall = smushMatrix(accMat, regType, time)
		plotMatrices(accMat, accMatSmall, time, regType)
		

printMatrices()


