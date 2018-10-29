'''
Counts the number of non-zero features were present

Use this to compare to the nonlinear model feature heatmap thing. 

'''

import csv
import matplotlib.pylab as plt
import numpy as np
import sklearn.linear_model


DATA_PATH = '../../data/'



tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']

dimensions=["acc_x", "acc_y", "acc_z", "mag_x", "mag_y", "mag_z", "gyro_x", "gyro_y", "gyro_z"]


def getFileName(task, subject, take, time):
	fileName = task + '_' + subject + '_' + take + '_Z'		
	if time != '':			# If the time is not all, then add the time description to the file name
		fileName += '_' + time
	fileName += '.csv'
	return fileName

def loadData(fileName):
	# Load the data into a numpy array of floats
	data = np.array(list(csv.reader(open(DATA_PATH + fileName,'r')))).astype(float)
	return data


	

def doRegression(X, y, reg = sklearn.linear_model.LinearRegression()):
	reg.fit(X, y)
	b = []
	b = [reg.intercept_]	# intercept will be first (a constant)
	b = b + list(reg.coef_)
	return b


def plotFeatures(data, time, regType):
	plt.matshow(data.T, aspect='auto')
	plt.colorbar(label='Feature Beta Weights')

	plt.title('Beta Weights: ' + time + ',' + regType)
	plt.xlabel('Subjects and Tasks')
	plt.xticks(range(15,150, 30), tasks)
	for i in range(len(tasks)):
		plt.axvline(i*(6)*(5)-0.5, color='k', linewidth=2.0)

	for i in range(4,150,5):
		plt.axvline(i+0.5, color='k', linewidth=1.0, linestyle='--')

	plt.ylabel('Device')
	plt.yticks(range(len(dimensions)), dimensions)
	for i in range(0, len(dimensions), 3):
		plt.axhline(i-.5, color='k', linewidth=2.0)
	plt.show()



def betaWeightMatrix(regType = 'OLS'):

	for time in times:
		betaWeights = []
		for task in tasks:
			for subject in subjects:
				for take in takes:
					# reporting
					print time, task, subject, take

					# Load the data
					fileName = getFileName(task, subject, take, time)
					data = loadData(fileName)

					# X is the independent variables (regressors)
					# y is the dependent variable
					# remember, we want: y = bX + e
					X = data[:, :-1]	
					y = data[:, -1]



					# do regression
					if regType == 'LASSO':
						reg = sklearn.linear_model.Lasso(alpha=0.1)
					else:
						reg = sklearn.linear_model.LinearRegression()

					b = doRegression(X, y, reg=reg)

					betaWeights.append(b[1:] + [1])		# remember, first col is intercept

		np.savetxt('2-beta_' + time + '_' + regType + '.csv', betaWeights, delimiter=',')
		
		betaWeights = np.array(betaWeights)
		plotFeatures(betaWeights, time, regType)
		#plt.matshow(betaWeights.T)
		#plt.show()

betaWeightMatrix('OLS')
betaWeightMatrix('LASSO')
