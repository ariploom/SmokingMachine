from numpy import *
from matplotlib.pyplot import *
from analyze_raw_data import *

def compare_samples(*samples, supress_plots=False):
	figure1 = figure()
	rg_plot = figure1.add_subplot(211)
	dam_plot = figure1.add_subplot(212)

	figure2 = figure()
	N_plot = figure2.add_subplot(211)
	c_plot = figure2.add_subplot(212)

	for s in samples:
		read_file = 'processed_data/' + s + '.csv'
		data = genfromtxt(read_file, delimiter=',')

		time = data[:,0]
		rg = data[:,1]
		N = data[:,2]
		dam = data[:,3]
		c = data[:,4]

		rg_plot.plot(time, rg)
		dam_plot.plot(time, dam)
		N_plot.semilogy(time,N)
		c_plot.plot(time,c)

	if supress_plots == False:
		show()
		return None
	else:
		return [figure1, figure2]