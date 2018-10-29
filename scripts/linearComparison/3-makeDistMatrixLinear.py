'''
Creates the distance/error/or whatever we want to call it matrix for the LINEAR models

'''

import csv
import numpy as np
import sklearn.linear_model

import linear_models_OLS
import linear_models_LASSO


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

def meanAbsoluteError(a, b):
	return abs(a - b)

def getModelErrorOnData(model, data, metrix=meanAbsoluteError):
	error = []
	for d in data:
		try:
			error.append(metrix(d[-1], model(*d[:-1])))	
		except Exception:
			print 'busted'
			error.append(np.float('nan'))

	return np.nanmean(error)

def getErrorForDataOnAllModels(functions, data, time, metrix=meanAbsoluteError):
	# mean absolute error list to be added to the matrix (this will be the rows)
	function_MAE = []
	
	# go through each function that was created
	for task in tasks:
		for subject in subjects:
			for take in takes:
				MAE = getModelErrorOnData(functions[time][task][subject][take], data, meanAbsoluteError)
				function_MAE.append(MAE)

	return function_MAE

def generateMatrix(functions, regType):

	for time in times:

		# Where we will store the mean absolute error matrix
		matrix_MAE = []
		for task in tasks:
			for subject in subjects:
				for take in takes:

					# reporting
					print time, task, subject, take

					# Load the data
					fileName = getFileName(task, subject, take, time)
					data = loadData(fileName)

					# get the mean absolute error for the data when applied to every model
					data_MAE = getErrorForDataOnAllModels(functions, data, time, meanAbsoluteError)					
			
					matrix_MAE.append(data_MAE)
		np.savetxt('3-matrix_' + time + '_' + regType + '.csv', matrix_MAE, delimiter=',')



DATA_PATH = '../../data/'




tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']
				
			
functions_OLS = linear_models_OLS.getFuncs()
functions_LASSO = linear_models_LASSO.getFuncs()

generateMatrix(functions_OLS, 'OLS')
generateMatrix(functions_LASSO, 'LASSO')
