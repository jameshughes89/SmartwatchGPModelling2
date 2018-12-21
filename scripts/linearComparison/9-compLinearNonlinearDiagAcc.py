'''
Compares the model accuracy on the diagonals. Linear vs Nonlinear. 

Will work with the smushed ones that do not apply the data the models were fit to to the models. 

'''



import csv
import numpy as np
import scipy
import sklearn.linear_model
import sys


DATA_PATH = '../../data/'



tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
#times =['']
times = ['', '10s', '20s']
#times = [sys.argv[1]]


NUM_FUNCTIONS = len(subjects)*len(tasks)*len(takes)


def getDiagonals(regType='OLS'):
	
	for time in times:
		print(time)
		# Linear
		linDistMat = np.array(list(csv.reader(open('./3-matrix_' + time + '_' + regType + '.csv','r')))).astype(float)

		linDiagValues = []
		for i in range(150):
			linDiagValues.append(linDistMat[i,i])


		smushLinDiagValues = []

		for i in range(0, 150, 5):
			for y in range(0, 5):
				for x in range(0, 5):
					if (i + y) != (i + x):
						smushLinDiagValues.append(linDistMat[i + y, i + x])

		# Nonlinear
		nonlinDistMat = np.array(list(csv.reader(open('./3-NLabEmat_' + time + '.csv','r')))).astype(float)
		
		nonlinDiagValues = []
		for i in range(150):
			nonlinDiagValues.append(nonlinDistMat[i,i])


		smushNonlinDiagValues = []

		for i in range(0, 150, 5):
			for y in range(0, 5):
				for x in range(0, 5):
					if (i + y) != (i + x):
						smushNonlinDiagValues.append(nonlinDistMat[i + y, i + x])


		print 'linear', np.mean(linDiagValues), np.median(linDiagValues), np.mean(smushLinDiagValues), np.median(smushLinDiagValues)
		print 'nonlinear', np.nanmean(nonlinDiagValues), np.nanmedian(nonlinDiagValues), np.nanmean(smushNonlinDiagValues), np.nanmedian(smushNonlinDiagValues)
		print 'MWU', scipy.stats.mannwhitneyu(linDiagValues, nonlinDiagValues), scipy.stats.mannwhitneyu(smushLinDiagValues, smushNonlinDiagValues)
		print




getDiagonals(regType='OLS')
print
print
getDiagonals(regType='LASSO')
