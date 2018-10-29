'''
Prints out the distance matrices generated in script 3.

You might have to change V_MIN and V_MAX


'''

import csv
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import sklearn.linear_model


DATA_PATH = './'

# Change these to alter the scales
V_MIN = 0		
V_MAX = 2.0


tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']


def plotMatrices(abeMat, avgMat_TAKE, avgMat_TASK, time, regType):
	pltz = []

	axes = plt.subplot2grid((1,3), (0,0))
	pltz.append(axes)
	img = pltz[0].matshow(abeMat, vmin=V_MIN, vmax=V_MAX)

	for i in range(30, 121, 30):
		pltz[0].axvline(i - 0.5, color='k', linewidth=2)
		pltz[0].axhline(i - 0.5, color='k', linewidth=2)

	for i in range(5, 151, 5):
		pltz[0].axvline(i - 0.5, color='k', linewidth=1, linestyle='--')
		pltz[0].axhline(i - 0.5, color='k', linewidth=1, linestyle='--')



	pltz[0].set_title('Each Dataset Applied to All Models', fontsize=12)
	pltz[0].set_ylabel('Data',rotation=90)
	pltz[0].set_xlabel('Model')
	pltz[0].set_yticks(range(15,150,30))
	pltz[0].set_yticklabels(tasks, rotation=90)
	pltz[0].set_xticks(range(15,150,30))
	pltz[0].set_xticklabels(tasks, rotation=0)

	divider = make_axes_locatable(axes)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(img, cax = cax)


	axes = plt.subplot2grid((1,3), (0,1))
	pltz.append(axes)
	img = pltz[1].matshow(avgMat_TAKE, vmin=V_MIN, vmax=V_MAX)

	for i in range(6, 30, 6):
		pltz[1].axvline(i - 0.5, color='k', linewidth=2)
		pltz[1].axhline(i - 0.5, color='k', linewidth=2)

	for i in range(1, 30, 1):
		pltz[1].axvline(i - 0.5, color='k', linewidth=1, linestyle='--')
		pltz[1].axhline(i - 0.5, color='k', linewidth=1, linestyle='--')



	pltz[1].set_title('Averaged Over Takes', fontsize=12)
	#pltz[1].set_ylabel('Data',rotation=90)
	pltz[1].set_xlabel('Model')
	pltz[1].set_yticks(range(2,30,6))
	pltz[1].set_yticklabels(tasks, rotation=90)
	pltz[1].set_xticks(range(2,30,6))
	pltz[1].set_xticklabels(tasks, rotation=0)
	divider = make_axes_locatable(axes)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(img, cax = cax)

	axes = plt.subplot2grid((1,3), (0,2))
	pltz.append(axes)
	img = pltz[2].matshow(avgMat_TASK, vmin=V_MIN, vmax=V_MAX)


	for i in range(1, 6, 1):
		pltz[2].axvline(i - 0.5, color='k', linewidth=2)
		pltz[2].axhline(i - 0.5, color='k', linewidth=2)


	pltz[2].set_title('Averaged Over Tasks', fontsize=12)
	#pltz[2].set_ylabel('Data',rotation=90)
	pltz[2].set_xlabel('Model')
	pltz[2].set_yticks(range(0,5,1))
	pltz[2].set_yticklabels(tasks, rotation=90)
	pltz[2].set_xticks(range(0,5,1))
	pltz[2].set_xticklabels(tasks, rotation=0)
	divider = make_axes_locatable(axes)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	plt.colorbar(img, cax = cax, label='Mean Absolute Error (limited at 2)')
	#plt.colorbar(img, label='Mean Absolute Error (limited at 2)')

	#plt.colorbar(label='Mean Absolute Error (limited at 2)', cax=pltz[0])
	#plt.tight_layout()

	# didnt work well with matshow
	plt.suptitle('Error Matrix: ' + time + ', ' + regType, fontsize=16)
	plt.show()


def printMatrices(regType = 'OLS'):
	for time in times:
		abeMat = np.array(list(csv.reader(open(DATA_PATH + '3-matrix_' + time + '_' + regType + '.csv','r')))).astype(float)
		
		# Average the matrix over the takes
		avgMat_TAKE = np.zeros((len(tasks) * len(subjects),len(tasks) * len(subjects)))
		for i in range(len(tasks) * len(subjects)):
			for j in range(len(tasks) * len(subjects)):
				avgMat_TAKE[i,j] = np.nanmean(abeMat[i * len(takes):(i+1)* len(takes),j * len(takes):(j+1)* len(takes)])

		# now average the matrix over the tasks
		avgMat_TASK = np.zeros((len(tasks),len(tasks)))
		for i in range(len(tasks)):
			for j in range(len(tasks)):
				avgMat_TASK[i,j] = np.nanmean(abeMat[i * len(takes) * len(subjects):(i+1)* len(takes) * len(subjects),j * len(takes) * len(subjects):(j+1)* len(takes) * len(subjects)])

		plotMatrices(abeMat, avgMat_TAKE, avgMat_TASK, time, regType)
		



printMatrices('OLS')
printMatrices('LASSO')
