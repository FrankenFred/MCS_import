#Script that consolidates data from several LIF decay data files in a directory and then tabulate into a separate text file


import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import sys

f = ""
filelist = []
save_arr = []
data_arr = []
#sigma_arr = []
time_arr = []
fit_arr = []
fit_file = "FIT_Coeffs.txt"
err_file = "Fit_Uncert.txt"
summ_file = "DAT_Summary.txt"
NoSave = True

#variables
plot_col = 2
time_step = 50 #time step in between each data point in micro seconds (us)

def div0( a, b ):
    #""" ignore / 0, div0( [-1, 0, 1], 0 ) -> [0, 0, 0] """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide( a, b )
        c[ ~ np.isfinite( c )] = 1  # -inf inf NaN
    return c

#fit function
def func(x, a, b, c):
	return a * np.exp(-b * x) + c
	
#fit function
def dexp_func(x, a, b, c, f, g):
	return (a * np.exp(-b * x)) + (f * np.exp(-g * x)) + c


	
#find all files with ".dat" ending
for file in os.listdir(os.getcwd()):
	if file.endswith(".dat"):
		f = str(file)
		filelist = np.append(filelist, f)

		
#set up plot...
plot_row = int((filelist.size+plot_col//2)//plot_col)
f, axarr = plt.subplots(plot_row,plot_col, figsize=((plot_col*4),(plot_row*3)),sharex=True)
axarr = axarr.ravel()
		
#For loop to extract data from each file and build save file list
for idx, item in enumerate(filelist):
	
	#build temporary list with data
	temp_arr = []
	temp_arr = np.genfromtxt(item, delimiter = '\t', dtype = 'str',)
	
	#convert data array to float for fitting - consider changing to import directly as float?!
	temp_arr = temp_arr.astype(np.float)
	time_arr, data_arr = np.hsplit(temp_arr, 2)	
	time_arr = time_arr.flatten()
	data_arr = data_arr.flatten()
	
	#trim the data array (sometimes the first few data points are rubbish) - currently 15 data points
	#data_arr = np.delete(data_arr, [0,1,2,3,4,5,6,7,8,9,10])

	data_arr = data_arr[5:900]
	time_arr = time_arr[5:900]
	#generate x axis (time)
	
	"""time_arr = np.zeros(len(data_arr))
	for i in range(0,len(time_arr)):
		time_arr[i] = i*(time_step*1e-6)
	
	#sigma = div0(1, data_arr)"""
	
	
	#fit data with func()
	popt, pcov = curve_fit(func, time_arr, data_arr, p0=(500,4000,20)) #, sigma=sigma, absolute_sigma=True
	error = [] 
	for i in range(len(popt)):
		try:
			error.append(np.absolute(pcov[i][i])**0.5)
		except:
			error.append( 0.00 )
	perr_curvefit = np.array(error)
	
	axarr[idx].scatter(time_arr, data_arr, s=5, facecolors='none', edgecolors='r')
	axarr[idx].set_xlim([np.amin(time_arr),np.amax(time_arr)])
	axarr[idx].plot(time_arr, func(time_arr,*popt))
	
	
	#if there's no save list yet, then set first set of data to save_arr. Otherwise, stack temp_arr with save_arr
	if NoSave:
		fit_arr = popt
		save_arr = data_arr
		err_arr = perr_curvefit
		NoSave = False
	else:
		save_arr = np.column_stack((save_arr,data_arr))
		err_arr = np.vstack((err_arr,perr_curvefit))
		fit_arr = np.vstack((fit_arr,popt))

#save data to text file.
save_file = open(summ_file, 'wb')	
np.savetxt(save_file, save_arr, delimiter = '\t',fmt="%s")
save_file.close()

#save fit coeffs to file
save_file = open(fit_file, 'wb')	
np.savetxt(save_file, fit_arr, delimiter = '\t',fmt="%s")
save_file.close()
#save fit uncerts to file
save_file = open(err_file, 'wb')	
np.savetxt(save_file, err_arr, delimiter = '\t',fmt="%s")
save_file.close()

#plot data
f.subplots_adjust(hspace=0)
#plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)	
plt.savefig('Data fit.png')