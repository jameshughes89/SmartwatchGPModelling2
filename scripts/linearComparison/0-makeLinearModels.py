'''
Creates linear models of the smart watch data. 

- Will do the linear models for all, 10s, and 20s
- Will generate standard linear modles
- Will generate LASSO linear models

- Output will be linear_models_TYPE (where type is the regression type)

'''

import csv
import numpy as np
import sklearn.linear_model


DATA_PATH = '../../data/'



tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']




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

def buildEquationToPrint(b):
	# start the equation as the intercept + the constant
	eqn = str(b[0]) + ' * 1 + '# + str(b[1]) + ' * 1 + '
	
	# build the expression
	for i in range(1, len(b)):
		eqn += str(b[i]) + ' * v[' + str(i-1) + ']'
		if i != len(b)-1:		# If we're not at the end of the equation, add a + sign
			eqn += ' + '
	return eqn

# didn't build this here because reasons...
def outputFiles(fileName):
	pass
	

def doRegression(X, y, reg = sklearn.linear_model.LinearRegression()):
	reg.fit(X, y)
	b = []
	b = [reg.intercept_]	# intercept will be first (a constant)
	b = b + list(reg.coef_)
	return b


def generateLinearModels(regType = 'OLS'):

	modelFile = open('./linear_models_' + regType + '.py','w')
	modelFile.write("from math import *\n\n")
	#errorFile = open('./linear_errors.py')
	
	# a dictionary to hold the dictionary for all functions
	modelFile.write('functions = {}\n')
	for time in times:

		# a dictionary to hold the dictionary for the tasks
		modelFile.write('task = {}\n')
		for task in tasks:

			# a dictionary to hold the dictionary for the subject's takes
			modelFile.write('subject = {}\n')
			for subject in subjects:
				
				# a dictionary to hold the functions for the takes
				modelFile.write('take = {}\n')
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

					# build the model and output it to a python friendly file
					eqn = buildEquationToPrint(b)
					function = 'def func_' + task + '_' + subject + '_' + take + '_' + time + '_' + regType + '(*v): return ' + eqn + '\n'
					modelFile.write(function)
					modelFile.write('take[\'' + take + '\'] = func_' + task + '_' + subject + '_' + take + '_' + time + '_' + regType + '\n')

				
				# add the dictionaries to the proper places
				modelFile.write('subject[\'' + subject + '\'] = take\n\n')
			modelFile.write('task[\'' + task + '\'] = subject\n\n')
		modelFile.write('functions[\'' + time + '\'] = task\n\n')

	modelFile.write('\n\ndef getFuncs(): return functions\n')
	modelFile.close()


generateLinearModels('OLS')
generateLinearModels('LASSO')
