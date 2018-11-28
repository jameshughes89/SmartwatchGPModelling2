'''
Creates a file containing ALL of the models. Will be stored in a dictionary. 
time, task, subject, take, MODEL_NUM

- Output will be nonlinear_models_vote

'''


# Open stats file
# Sort (argsort?)
# load up functions
# put into dictionary

import csv
import numpy as np
import sklearn.linear_model


DATA_PATH = '../../data/'



tasks = ['Up', 'Down', 'Walking',  'Jogging', 'Running',]
subjects = ['1','2','3','4','5','6']
takes = ['1','2','3','4','5']
times = ['', '10s', '20s']

def collectNonlinearModels():

	modelFile = open('./nonlinear_models_vote.py','w')
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
					if time == '':
						tme = 'all'			# Have to do this because of inconsistent nameing of all/''
					else:
						tme = time
					stats = np.array(list(csv.reader(open('./../../outsSM_' + tme + '/' + task + '_' + subject + '_' + take + '_Z_' + tme + '/stats.csv', 'r')))).astype(float)[:, 1]		# Col 0 is just a count, so we want all rows from col 1
					
					# This will get the array that orders the functions in order of lowest MAE
					# Will use this to order the functions in our dictionary best to worst. 
					# Might not care about this, but who knows
					functionRanks = np.argsort(stats)

					# A dictionary that will hold all 100 models for each task/subject/take
					# The order will be in order of lowest MAE to highest on TRAINING DATA
					modelFile.write('ordered = {}\n')
					
					# For each of the functions, in order of MAE					
					for i, rank in enumerate(functionRanks):

						# Find the corresponding function file
						funcFile = open('./../../outsSM_' + tme + '/' + task + '_' + subject + '_' + take + '_Z_' + tme + '/' + str(rank) + '_line.txt','r')
						
						# Read the line, and replace any 'e(' with an 'exp('
						eqn = funcFile.next().replace('e(', 'exp(')
						
						modelFile.write('def func_' + str(rank) + '_' + task + '_' + subject + '_' + take + '_' + time + '(v0,v1,v2,v3,v4,v5,v6,v7,v8): return ' + eqn + '\n')
						modelFile.write('ordered[' + str(i) + '] = func_' + str(rank) + '_' + task + '_' + subject + '_' + take + '_' + time + '\n')
					
					# add the dictionaries to the proper places
					modelFile.write('take[\'' + take + '\'] = ordered\n\n')
				modelFile.write('subject[\'' + subject + '\'] = take\n\n')
			modelFile.write('task[\'' + task + '\'] = subject\n\n')
		modelFile.write('functions[\'' + time + '\'] = task\n\n')

	modelFile.write('\n\ndef getFuncs(): return functions\n')
	modelFile.close()


collectNonlinearModels()
