'''
Print out the accuracy curve.


'''

import csv
import math
import matplotlib as mpl
import matplotlib.pylab as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import sklearn.linear_model
import sys

mpl.style.use('classic')


tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
#times = ['']
times = ['', '10s', '20s']
#times = [sys.argv[1]]


NUM_FUNCTIONS = len(subjects)*len(tasks)*len(takes)


# Probably leave them as 0 -- 1
V_MIN = 0.0		
V_MAX = 1.0




def printAccCurve(regType = 'OLS'):
	for time in times:
		curveData = np.array(list(csv.reader(open('./5-accCurveNoSameTake-' + time + '_' + regType + '.csv','r')))).astype(float)
		CIi = []
		CIa = []
		for l in curveData:
			CIi.append(l[0] - (1.96 * (l[1]/math.sqrt(l[5]))))
			CIa.append(l[0] + (1.96 * (l[1]/math.sqrt(l[5]))))


		#plt.axhline(1.2)
		
		# Set up dashed lines
		for y in np.arange(0.1, 1.11, 0.1):
			plt.axhline(y, color='k', ls='--', alpha=0.25)

		Xs = range(5,121,5)
		
		plt.plot(Xs,curveData[:,4], label='Maximum')
		plt.plot(Xs,curveData[:,2], label='Median')
		plt.plot(Xs,curveData[:,0], label='Mean')
		plt.plot(Xs, CIi, 'k', alpha=0.2, label='95% Confidence Interval')
		plt.plot(Xs, CIa, 'k', alpha=0.2)
		plt.fill_between(Xs, CIi, CIa, facecolor='k', alpha = 0.1)
		plt.plot(Xs,curveData[:,3], label='Minimum')

		plt.title('Accuracy Curves for ' + time + ',' + regType)
		plt.legend(loc='best')
		plt.xlabel('Time Points')
		plt.ylabel('Accuracy')
		plt.show()

printAccCurve()

