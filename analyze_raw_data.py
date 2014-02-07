#!/usr/bin/env python

from numpy import *
from calc_rg import *
from matplotlib.pyplot import *

def analyze_raw_data(experiment):
	filename = 'raw_data/' + experiment + '.csv'
	data = genfromtxt(filename, delimiter=',')
	
	puff_volume = data[0,0]
	puff_duration = data[0,1]
	num_puffs = data[0,2]

	time = squeeze(data[1:len(data),0])
	intensities = data[1:len(data),1:5]

	puff_times = []
	for t in range(len(time)):
		if data[t,7] != 0:
			puff_times.append(time[t])

	absorbtions = empty_like(intensities)
	wavelengths = array([550., 650., 750., 850.])
	base_intensities = average(intensities[0:250, :], axis=0)
	print base_intensities.shape


	for t in range(len(time)):
		for l in range(len(wavelengths)):		
			absorbtions[t,l] = log(base_intensities[l]/intensities[t,l])

	print absorbtions[800,:]

	plot(time, absorbtions)
	show()







analyze_raw_data('A0004A')