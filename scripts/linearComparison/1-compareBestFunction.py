'''
Plots the best function on all data from that subject/task
Same as script from project iteration 1, but this time we plot against linear


'''

import csv
from math import *
import matplotlib.pylab as plt
import numpy as np

# function for Running, subject 6, take 2:
def func_146(v0,v1,v2,v3,v4,v5,v6,v7,v8): return  ( ( ( ( (exp( v0 )+ ( v1 - 7.8727996162556195 ) ) / (exp( v1 )+ 7.8727996162556195 ) ) + ( (sin( v6 )/ 4.417633692471078 ) /exp( v0 )) ) *sin( (sin( v6 )+sin( v6 )) )) + ( ( ( v1 - ( (sin( v6 )/ 4.417633692471078 ) /exp( v0 )) ) / ( (exp( v1 )+ 7.8727996162556195 ) / 4.417633692471078 ) ) + ( (sin( v6 )*sin( v6 )) / ( -3.9969789375939904 - v1 ) ) ) ) 

# Same as above, but from ols
def func_Running_6_2_OLS(*v): return 3.51654665609e-14 * 1 + 0.0 * 1 + 0.0834192820844 * v[0] + 0.355599067263 * v[1] + -0.0632027017302 * v[2] + -0.0316450056136 * v[3] + 0.0384212109926 * v[4] + -0.0273187737169 * v[5] + -0.794628395732 * v[6] + -0.0310839822898 * v[7]

# Same as above, but from lasso
def func_Running_6_2_LASSO(*v): return 1.18047638688e-14 * 1 + 0.0 * v[0] + 0.290296531988 * v[1] + -0.0 * v[2] + -0.0 * v[3] + 0.0 * v[4] + -0.0 * v[5] + -0.729330283306 * v[6] + -0.00890178576675 * v[7]

pltz = []
pltz.append(plt.subplot2grid((3,2), (0,0), colspan=2))
plt.title("Subject 6 Running Take 2 --- Model Fit To This Data")
plt.xlabel("Time Point")
plt.ylabel("Signal Intensity")
pltz.append(plt.subplot2grid((3,2), (1,0)))

pltz.append(plt.subplot2grid((3,2), (1, 1)))

pltz.append(plt.subplot2grid((3,2), (2, 0)))

pltz.append(plt.subplot2grid((3,2), (2, 1)))


takes = [2,1,3,4,5]

for i in range(len(takes)):

	iFile = csv.reader(open('../../data/Running_6_' + str(takes[i]) + '_Z.csv', 'r'))
	data = []
	for l in iFile:
		data.append(l)
	data = np.array(data)
	data = data.astype(np.float)
	signal = data.T[-1]
	expected = []
	expected_OLS = []
	expected_LASSO = []
	err = []
	err_OLS = []
	err_LASSO = []
	for r in data:
		expected.append(func_146(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8]))
		expected_OLS.append(func_Running_6_2_OLS(*r[:-1]))
		expected_LASSO.append(func_Running_6_2_LASSO(*r[:-1]))
		err.append(abs(r[8] - expected[-1]))
		err_OLS.append(abs(r[8] - expected_OLS[-1]))
		err_LASSO.append(abs(r[8] - expected_LASSO[-1]))

	print np.mean(err), np.mean(err_OLS), np.mean(err_LASSO)
	if i == 0:
		pltz[i].set_title("Subject 6 Running Take " + str(takes[i]) + " --- Model Fit To This Data")
	else:
		pltz[i].set_title("Subject 6 Running Take " + str(takes[i]))

	if i != 1 and i != 2:
		pltz[i].set_xlabel("Time Point")
	pltz[i].set_ylabel("Gyro_z Signal")
	pltz[i].plot(signal, label='Signal')
	#pltz[i].scatter(range(len(signal)),signal)
	pltz[i].plot(expected, label='Nonlinear')
	pltz[i].plot(expected_OLS, label='OLS')
	pltz[i].plot(expected_LASSO, label='LASSO')
	pltz[i].legend(fontsize=8)


#plt.tight_layout()
plt.show()
