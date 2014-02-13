from numpy import *
from calc_rg import *
from matplotlib.pyplot import *

def analyze_raw_data(experiment, suppress_plot=False):
	read_file = 'raw_data/' + experiment + '.csv'
	data = genfromtxt(read_file, delimiter=',')
	
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
	rg = empty_like(time)
	m = empty_like(time)
	sg = empty_like(time)
	k = empty_like(absorbtions)
	error = empty_like(time)
	N = empty_like(time)
	dam = empty_like(time)
	c = empty_like(time)
	b = 16*.1/(3*pi) #path length of light in cm
	rho = 1.19 #g/cc assuming 70/30 vg/pg

	for t in range(len(time)):
		for l in range(len(wavelengths)):		
			absorbtions[t,l] = log(base_intensities[l]/intensities[t,l])
		if max(absorbtions[t,:]) > .06:
			crunched_absorbtions = calc_rg(absorbtions[t,:])
			rg[t] = crunched_absorbtions[0]
			m[t] = crunched_absorbtions[1]
			sg[t] = crunched_absorbtions[2]
			k[t,:] = crunched_absorbtions[3]
			error[t] = crunched_absorbtions[4]

			n = 0
			for l in range(len(wavelengths)):
				n += absorbtions[t,l]/(k[t,l]*b)
			N[t] = n/len(wavelengths) # particles/cc
			dam[t] = 2*rg[t]*exp(1.5*(log(sg[t])**2)) # ug
			c[t] = 1000*N[t]*rho*(pi/6)*(dam[t]*.0001)**3 #mg/cc
		else:
			rg[t] = 0
			m[t] = 0
			sg[t] = 0
			k[t,:] = 0
			error[t] = 1
			N[t] = 0
			dam[t] = 0
			c[t] = 0


	write_data = transpose(array([
		time,
		rg,
		N,
		dam,
		c,
		m,
		sg,
		squeeze(k[:,0]),
		squeeze(k[:,1]),
		squeeze(k[:,2]),
		squeeze(k[:,3]),
		error]))
	write_file = 'processed_data/' + experiment + '.csv'
	savetxt(write_file, write_data, delimiter=",")

	if suppress_plot == False:
		figure(1)
		subplot(211)
		plot(time, rg)
		subplot(212)
		plot(time, dam)

		figure(2)
		subplot(211)
		semilogy(time, N)
		subplot(212)
		plot(time,c)

		show()