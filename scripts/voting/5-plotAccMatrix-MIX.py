'''
Plot the accuracy matrices (big and small). This is also like a confusion mattrix. 

MIX

'''

import csv
import numpy as np
import sys

import matplotlib as mpl
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

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


# Create a plot for each time
for time in times:

	for voters in range(NUM_VOTERS_START, NUM_VOTERS_STOP + 1):
		fName = '3-AccMat-MIX_' + str(voters) + '_' + str(GROUP_SIZE) + '_' + time + '.csv'
		largeMat = loadData(fName)
		for i in range(len(largeMat)):
			largeMat[i,i] = float('nan')

		fName = '3-AccMat-Small-MIX_' + str(voters) + '_' + str(GROUP_SIZE) + '_' + time + '.csv'
		smallMat = loadData(fName)

		pltz = []

		axes = plt.subplot2grid((1,2), (0,0))
		pltz.append(axes)

		img = pltz[0].matshow(largeMat)

		#plt.clim(0,1)

		pltz[0].set_yticks(range(15,150,30))
		pltz[0].set_yticklabels(tasks, rotation=90)
		pltz[0].set_xticks(range(15,150,30))
		pltz[0].set_xticklabels(tasks, rotation=0)


		for i in range(29, 150,30):
			pltz[0].axvline(i+0.5, color='k', linewidth=2)	
			pltz[0].axhline(i+0.5, color='k', linewidth=2)

		for i in range(4,150,5):
			pltz[0].axvline(i+0.5, color='k', linewidth=1, linestyle='--')
			pltz[0].axhline(i+0.5, color='k', linewidth=1, linestyle='--')


		#pltz[0].set_title('Accuracy Matrix: Each Dataset Applied to All Models Except Self --- ' + TIME + ' (Batch of ' + str(GROUP_SIZE) + ')')

		pltz[0].set_ylabel('Data',rotation=90)
		pltz[0].set_xlabel('Model')

		divider = make_axes_locatable(axes)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		plt.colorbar(img, cax = cax)
		#plt.clim(0,1)
		#plt.show()


		axes = plt.subplot2grid((1,2), (0,1))
		pltz.append(axes)

		img = pltz[1].matshow(smallMat, aspect='auto')


		pltz[1].set_yticks(range(15, 150,30))
		pltz[1].set_yticklabels(tasks, rotation=90)
		pltz[1].set_xticks(range(2,30,6))
		pltz[1].set_xticklabels(tasks, rotation=0)

		for i in range(29, 150,30):
			pltz[1].axhline(i+0.5, color='k', linewidth=2)

		for i in range(5,30,6):
			pltz[1].axvline(i+0.5, color='k', linewidth=2)

		for i in range(4,150,5):
			pltz[1].axhline(i+0.5, color='k', linewidth=1, linestyle='--')


		pltz[1].set_ylabel('Data',rotation=90)
		pltz[1].set_xlabel('Model')

		divider = make_axes_locatable(axes)
		cax = divider.append_axes("right", size="5%", pad=0.05)
		plt.colorbar(img, cax = cax)

		if time == '':
			name = 'all'
		else:
			name = time	
		plt.suptitle('Confusion Matrix --- Mix: ' + name + ', ' + str(voters) + ' voter(s)',fontsize=16)
		plt.show()














			
