'''
Generates an accuracy table like the in the 2018 CIBCB paper. 

It will be a table for a specific time, group size/time points, and voters. 

RAND
'''

import csv
import numpy as np
import scipy.stats 

DATA_PATH = './accuracyMatrices/'


tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']
#times = ['']
#times = [sys.argv[1]]


# CHANGE THESE!
GROUP_SIZE = 50
VOTERS = 1

def loadData(fileName):
	# Load the data into a numpy array of floats
	data = np.array(list(csv.reader(open(DATA_PATH + fileName,'r')))).astype(float)
	return data


def calcCI(a):
	return scipy.stats.norm.interval(0.95, loc=np.mean(a), scale=(np.std(a)/np.sqrt(len(a))))[1] - np.mean(a)	# return 1 because 0 is the negative

def calcIQR(a):
	q75, q25 = np.percentile(a, [75 ,25])
	return q75 - q25

# Create a plot for each time
for time in times:
	
	print time
	# Load up the small acc mats
	fName = '2-AccMat-Small-RAND_' + str(VOTERS) + '_' + str(GROUP_SIZE) + '_' + time + '.csv'
	smallMat = loadData(fName)
	
	# Generate a matrix with how often data 
	# from a task (regardless of subject)
	# was picked by a model of the same task
	taskMat = []
	for i in range(0, smallMat.shape[0], 1):
		row = []
		for j in range(0, smallMat.shape[1], 6):
			row.append(np.sum(smallMat[i, j:j+6]))
		taskMat.append(row)
	
	taskMat = np.array(taskMat)	


	# Generate a matrix with how often data 
	# from a subject (regardless of task)
	# was picked by a model of the same subject
	subjectMat = []
	for i in range(0, smallMat.shape[0], 5):
		row = []
		for j in range(smallMat.shape[1]):
			row.append(np.mean(smallMat[i:i+len(takes), j]))
		subjectMat.append(row)

	subjectMat = np.array(subjectMat)

	totalAccuracy = []
	taskAccuracy = []
	subjectAccuracy = []

	# Make the table (latex format)
	for i, task in enumerate(tasks):
		# String we're building for output
		s = '' + task + ' &\t '
		for j, sub in enumerate(subjects):
			#print '(' + str(i * (len(tasks) * len(subjects)) + len(takes) * j) +  ':' + str(i * (len(tasks) * len(subjects) + len(takes) * j + len(takes))) + ', ' + str( i * len(subjects) + j) + ')\t', smallMat[i * (len(tasks) * len(subjects)) + j * len(takes):i * (len(tasks) * len(subjects)) + j * len(takes) + len(takes), i * len(subjects) + j]
			# Switch this for mean/median and CI/IQR
			# This is mean +- CI
			s += str(round(np.mean(smallMat[i * (len(tasks) * len(subjects)) + j * len(takes):i * (len(tasks) * len(subjects)) + j * len(takes) + len(takes), i * len(subjects) + j]), 3)) 
			s += ' $\pm$ '+ str(round(calcCI(smallMat[i * (len(tasks) * len(subjects)) + j * len(takes):i * (len(tasks) * len(subjects)) + j * len(takes) + len(takes), i * len(subjects) + j]), 3))
			totalAccuracy.append(np.mean(smallMat[i * (len(tasks) * len(subjects)) + j * len(takes):i * (len(tasks) * len(subjects)) + j * len(takes) + len(takes), i * len(subjects) + j]))
			# This is median +- IQR
			#s += str(round(np.median(smallMat[i * (len(tasks) * len(subjects)) + j * len(takes):i * (len(tasks) * len(subjects)) + j * len(takes) + len(takes), i * len(subjects) + j]), 3)) 
			#s += ' $\pm$ '+ str(round(calcIQR(smallMat[i * (len(tasks) * len(subjects)) + j * len(takes):i * (len(tasks) * len(subjects)) + j * len(takes) + len(takes), i * len(subjects) + j]), 3))
			#totalAccuracy.append(np.median(smallMat[i * (len(tasks) * len(subjects)) + j * len(takes):i * (len(tasks) * len(subjects)) + j * len(takes) + len(takes), i * len(subjects) + j]))
			s += '\t& '
		
		# For mean _- CI
		s += str(round(np.mean(taskMat[i * (len(takes) * len(subjects)): (i+1) * (len(takes) * len(subjects)), i]), 3))
		s += ' $\pm$ '+ str(round(calcCI(taskMat[i * (len(takes) * len(subjects)): (i+1) * (len(takes) * len(subjects)), i]), 3))
		taskAccuracy.append(np.mean(taskMat[i * (len(takes) * len(subjects)): (i+1) * (len(takes) * len(subjects)), i]))
		# This is median +- IQR
		#s += str(round(np.median(taskMat[i * (len(takes) * len(tasks) * len(subjects)): (i+1) * (len(takes) * len(tasks) * len(subjects)), i)), 3))
		#s += ' $\pm$ '+ str(round(calcIQR(taskMat[i * (len(takes) * len(tasks) * len(subjects)): (i+1) * (len(takes) * len(tasks) * len(subjects)), i)), 3))
		#taskAccuracy.append(np.median(taskMat[i * (len(takes) * len(subjects)): (i+1) * (len(takes) * len(subjects)), i])


		s += '\\\\'
		print s

	s = 'Identify Subject &\t '
	for i, sub in enumerate(subjects):
		curSub = []
		for j in range(0,5):
			curSub.append(np.sum([subjectMat[j*6+i,0+i], subjectMat[j*6+i,6+i], subjectMat[j*6+i,12+i], subjectMat[j*6+i,18+i], subjectMat[j*6+i,24+i]]))

		# This is mean +- CI
		s += str(round(np.mean(curSub), 3))
		s += ' $\pm$ '+ str(round(calcCI(curSub), 3))
		subjectAccuracy.append(np.mean(curSub))
		# This is median +- IQR
		#s += str(round(np.median(curSub), 3))
		#s += ' $\pm$ '+ str(round(calcIQR(curSub), 3))
		#subjectAccuracy.append(np.median(curSub))

		s += '\t& '

	s += '\\\\'
	print s

	print '------------------'
	print 'Overall Accuracy:', np.mean(totalAccuracy)
	print 'Task Accuracy:', np.mean(taskAccuracy)
	print '\tWalking-ish', np.mean(np.sum(taskMat[:90,:3],axis=1))
	print '\tRunning-ish', np.mean(np.sum(taskMat[90:,3:],axis=1))
	print 'Subject Accuracy:', np.mean(subjectAccuracy) 

	print '\n\n\n'














			
