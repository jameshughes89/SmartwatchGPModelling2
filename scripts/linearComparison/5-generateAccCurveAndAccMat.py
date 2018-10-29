'''
Generates the accuracy curve for the data based on the number of data poitns in GROUP SIZE
Also generates the accuracy matrices too. 

*
****************
NOTE TO JAMES:
		What if there was a curve for each task? May emphasize what tasks suck?
****************
*

**** IMPORTANT NOTE IF USING THIS SCRIPT AGAIN IN THE FUTURE! ****
(Might kinda' ruin the randomness though... so, idk)
I have a strong feeling that I could make this WAY FASTER IF:
- Only calculate on the max value of GROUP_SIZE (120 in this case)
- Store all the values, so I have a 120 rows x 100 cols
- Calculate each GROUP_SIZE's error by doing the mean of the first 5, 10, 15, 20, 25, etc. rows
- I'm pretty sure that will work, and it will make it run WAY FASTER!


'''

import csv
import numpy as np
import sklearn.linear_model
import sys

import linear_models_OLS
import linear_models_LASSO



DATA_PATH = '../../data/'



tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
#times = ['', '10s', '20s']
times = [sys.argv[1]]


NUM_FUNCTIONS = len(subjects)*len(tasks)*len(takes)

functions_OLS = linear_models_OLS.getFuncs()
functions_LASSO = linear_models_LASSO.getFuncs()


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


def generateAccCurve(functions, regType = 'OLS'):

	for time in times:

		# A list to hold the details for the accuracy curve
		# This will be saved and printed out later. 
		accCurveState = []

		# How many data points are used for classification?
		# start at 5, count by 5s to 121 (121 is overkill)
		for GROUP_SIZE in range(5, 121, 5):
	
			# This is where we will store all the data to be output
			accMat = []	
	
			for task in tasks:
				for subject in subjects:
					for take in takes:

						# reporting
						print time, GROUP_SIZE, ':\t', task, subject, take

						# Load the data
						# We're always applying it to the full data (all --- '')
						fileName = getFileName(task, subject, take, '')
						data = loadData(fileName)

						# Store a row (corresponding to a set of data) of accuracies
						# This will be added to the accMat
						accRow = np.zeros(NUM_FUNCTIONS)

						# We'll repeat the test 100 times (ti give us a percent)
						# Basically, apply some subset of data (GROUP_SIZE) to models 100 times.
						# This is for the stats. This makes sense... right?
						for i in range(100):
							
							# This list will store lists of errors
							# the length of this list depends on GROUP_SIZE
							# The lenfth of the lists inside this list will be equal to NUM_FUNCTIONS			
							# Eventually we will get the column mean, to know how each model did.
							absErr_forAllData = []

							# For each data point in a randomly selected set of data of size GROUP_SIZE
							# Apply this data point to each model, and keep track of the errors in a list
							# After applying this data point to every function, but that list inside ansErr_forAllData
							for d in data[np.random.permutation(len(data))[:GROUP_SIZE]]:
								absErr_forDatum = []
							
								# For each model... 
								# I really really wish I wrote this in a similar way to script 3
								# had to rename variables here to not mess with outer loops
								for tsk in tasks:
									for sub in subjects:
										for tke in takes:
											
											# NEVER APPLY THE DATA TO THE MODEL IT WAS FIT TOOO!!!
											# If we have data from the model we're looking at, skip it (add max value because that means it will never be the 'BEST')
											if task == tsk and subject == sub and tke == take:
												absErr_forDatum.append(sys.maxint)
											# Otherwise, just apply the data to the model and record the error value
											else:
												try:
													# Get the error by finding the difference between what we expect (l[-1] --- the last element in the row)
													# and what we got (applying all other data points to the model).
													err = d[-1] - functions[time][tsk][sub][tke](*d[:-1])
												except (ValueError, OverflowError, ZeroDivisionError):
													print 'Busted'
													err = float('nan')

												# Add the error to the list keeping track of the data points error on all models													
												absErr_forDatum.append(abs(err))

								# After applying the single row of data to all models
								# Add the error for each model to the list of errors
								# After doing this for all data points (GROUP_SIZE), we will get the column mean. 
								absErr_forAllData.append(absErr_forDatum)

							# This line should not be necessary....
							#if np.argmin(np.mean(abEs,axis=0)) > 0.000:	
							
							# Find the index of the model with the smallest error
							# This will be the *winner* model
							# And mark it as the winner in the row's accuracy
							# Note that this is not an accuracy really, but just a record that it was selected
							# Accuracy is determined if the min model belonged to the same subject/task combo (take doesn't matter)		
							accRow[np.argmin(np.mean(absErr_forAllData,axis=0))] += (1.)

						# Divide by 100 so we get a percent
						# Add the row's (data set's) values to the matrix
						# Remember, accuracy is really only measures after it's verified
						# Really, the matrix is just seeing what % of the time what model was the best.  
						accRow = accRow/float(100)
						accMat.append(accRow)

			accMat = np.array(accMat)

			# Save the accuracy matrix here
			np.savetxt('./accuracyMatrices/5-AccMat_' + str(GROUP_SIZE) + '_' + time + '_' + regType + '.csv', accMat, delimiter=',') 

			# This part will now count the actual accuracies
			
			# Where we will store the compressed version of the mat
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
			
			
			# Go through the diagonal (kinda, it's not really a diag, more like a staircase)					
			# And record how often it was right
			diagValues = []
			
			# This is ugly, but works...
			# 150 rows, 30 cols remember
			# So we need to look at 5 rows for each col. 
			for i in range(30):
				for j in range(5):
					diagValues.append(accMatSmall[i*5+j,i])		
			
			# Store the mean, standard deviation, median, min, max, and number of functions (for CI calculations)
			accCurveState.append([np.mean(diagValues), np.std(diagValues), np.median(diagValues), np.min(diagValues), np.max(diagValues), NUM_FUNCTIONS])

		# Save the output for each time 
		np.savetxt('5-accCurveNoSameTake-' + time + '_' + regType + '.csv', accCurveState, delimiter=',')
			

#generateAccCurve(functions_OLS, regType='OLS')
generateAccCurve(functions_LASSO, regType='LASSO')
