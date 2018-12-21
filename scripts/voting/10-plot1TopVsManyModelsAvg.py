'''
Generate a plot showing many models against the timeseries vs. a voteint system. 

'''

import csv
import matplotlib as mpl
import matplotlib.pylab as plt
import numpy as np
import sklearn.linear_model
import sys


import nonlinear_models_vote

mpl.style.use('classic')
DATA_PATH = '../../data/'



tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']
#times = [sys.argv[1]]


NUM_FUNCTIONS = len(subjects)*len(tasks)*len(takes)
NUM_VOTERS_START = 5
NUM_VOTERS_STOP = 10
MAX_GROUP_SIZE = 120

functions = nonlinear_models_vote.getFuncs()


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


# Load the data
# We're always applying it to the full data (all --- '')
fileName = getFileName('Running', '1', '1', '')
take1 = loadData(fileName)
fileName = getFileName('Running', '1', '2', '')
take2 = loadData(fileName)
fileName = getFileName('Running', '1', '3', '')
take3 = loadData(fileName)
fileName = getFileName('Running', '1', '4', '')
take4 = loadData(fileName)
fileName = getFileName('Running', '1', '5', '')
take5 = loadData(fileName)



subjectModels = functions['']['Running']['1']['1']


y = []
y_hat_single = []
y_hat_five_mean = []
y_hat_five_median = []
for d in take2 :
	y.append(d[-1])
	y_hat_single.append(subjectModels[0](*d))
	y_hat_five_mean.append(np.mean([subjectModels[0](*d), subjectModels[1](*d), subjectModels[2](*d), subjectModels[3](*d), subjectModels[4](*d)]))
	y_hat_five_median.append(np.median([subjectModels[0](*d), subjectModels[1](*d), subjectModels[2](*d), subjectModels[3](*d), subjectModels[4](*d)]))

y = np.array(y)
y_hat_single = np.array(y_hat_single)
y_hat_five_mean = np.array(y_hat_five_mean)
y_hat_five_median = np.array(y_hat_five_median)


print np.mean(abs(y - y_hat_single))
print 'five'
print np.mean(abs(y - y_hat_five_median))
print np.mean(abs(y - y_hat_five_mean))

plt.plot(y, label='Signal')
plt.plot(y_hat_single, label='Single Model - ' + str(round(np.mean(abs(y - y_hat_single)),3)))
plt.plot(y_hat_five_median, label='Five Model Median - ' + str(round(np.mean(abs(y - y_hat_five_median)),3)))



plt.legend(fontsize=8)
plt.xlabel('Time Point')
plt.ylabel('Gyro_z Signal')
plt.title('Subject 1 Running\nModels vs. Signal')
plt.show()










