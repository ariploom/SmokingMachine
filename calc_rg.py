from numpy import *

scattering_coefficients = empty([4, 21, 19, 100])

for l in range(scattering_coefficients.shape[0]):
	for sg in range(scattering_coefficients.shape[1]):
		filename = 'lookup_tables/lambda=' + str(l+1) + '_sigma=' + str(sg+1) + '.csv'
		scattering_coefficients[l,sg,:,:] = genfromtxt(filename, delimiter=',')

theoretical_ratios = empty([
	scattering_coefficients.shape[0]-1,
	scattering_coefficients.shape[1],
	scattering_coefficients.shape[2],
	scattering_coefficients.shape[3]
	])

for i in range(theoretical_ratios.shape[0]):
	for sg in range(theoretical_ratios.shape[1]):
		for m in range(theoretical_ratios.shape[2]):
			for rg in range(theoretical_ratios.shape[3]):
				if i == 0:
					l = i
				else:
					l = i + 1
				theoretical_ratios[i,sg,m,rg] = scattering_coefficients[l,sg,m,rg]/scattering_coefficients[1,sg,m,rg]


def calc_rg(absorbtions):

	experimental_ratios = array([
		absorbtions[0]/absorbtions[1], 
		absorbtions[2]/absorbtions[1], 
		absorbtions[3]/absorbtions[1]
		])

	radii = linspace(.01,1,100)
	refractive_indeces = linspace(1.33,1.51,19)
	sigmas = linspace(1.3,1.42,13)

	bounds = array([
		[0,len(radii)-1],
		[0,len(refractive_indeces)-1],
		[0,len(sigmas)-1]
		])

	error = 1

	while bounds[0,0] < bounds[0,1]:
		test_points = generate_test_points(bounds)
		best_fit = -1

		for i in range(len(test_points)):
			test_error = 0
			for j in range(len(experimental_ratios)):
				test_error += (experimental_ratios[j] - theoretical_ratios[j,test_points[i,2],test_points[i,1],test_points[i,0]])**2
			if test_error < error:
				error = test_error
				best_fit = i

		bounds = adjust_bounds(best_fit, bounds, test_points)

	return [
		radii[bounds[0,0]], 
		refractive_indeces[bounds[1,0]], 
		sigmas[bounds[2,0]], 
		dot(squeeze(scattering_coefficients[:,bounds[2,0],bounds[1,0],bounds[0,0]]),.0001**2),
		error]

def generate_test_points(bounds):
	r_mid = (bounds[0,0]+bounds[0,1])/2
	if bounds[2,0] < bounds[2,1]:
		s_mid = (bounds[2,0]+bounds[2,1])/2
		if bounds[1,0] < bounds[1,1]:
			m_mid = (bounds[1,0]+bounds[1,1])/2
			test_points = array([
				[(r_mid+bounds[0,0])/2,(m_mid+bounds[1,0])/2,(s_mid+bounds[2,0])/2],
				[(r_mid+bounds[0,1])/2,(m_mid+bounds[1,0])/2,(s_mid+bounds[2,0])/2],

				[(r_mid+bounds[0,0])/2,(m_mid+bounds[1,0])/2,(s_mid+bounds[2,1])/2],
				[(r_mid+bounds[0,1])/2,(m_mid+bounds[1,0])/2,(s_mid+bounds[2,1])/2],

				[(r_mid+bounds[0,0])/2,(m_mid+bounds[1,1])/2,(s_mid+bounds[2,1])/2],
				[(r_mid+bounds[0,0])/2,(m_mid+bounds[1,1])/2,(s_mid+bounds[2,0])/2],
				[(r_mid+bounds[0,1])/2,(m_mid+bounds[1,1])/2,(s_mid+bounds[2,0])/2],
				[(r_mid+bounds[0,1])/2,(m_mid+bounds[1,1])/2,(s_mid+bounds[2,1])/2]
				])

		else:
			test_points = array([
				[(r_mid+bounds[0,0])/2,bounds[1,0],(s_mid+bounds[2,0])/2],
				[(r_mid+bounds[0,1])/2,bounds[1,0],(s_mid+bounds[2,0])/2],

				[(r_mid+bounds[0,0])/2,bounds[1,0]/2,(s_mid+bounds[2,1])/2],
				[(r_mid+bounds[0,1])/2,bounds[1,0]/2,(s_mid+bounds[2,1])/2]
				])

	else:
		test_points = array([
			[(r_mid+bounds[0,0])/2,bounds[1,0],bounds[2,0]],
			[(r_mid+bounds[0,1])/2,bounds[1,0],bounds[2,0]]
			])

	return test_points

def adjust_bounds(best_fit, bounds, test_points):
	r_mid = (bounds[0,0]+bounds[0,1])/2
	m_mid = (bounds[1,0]+bounds[1,1])/2
	s_mid = (bounds[2,0]+bounds[2,1])/2
	
	if best_fit == 0:
		bounds[0,1] = r_mid
		bounds[1,1] = m_mid
		bounds[2,1] = s_mid
	elif best_fit == 1:
		bounds[0,0] = r_mid
		bounds[1,1] = m_mid
		bounds[2,1] = s_mid
	elif best_fit == 2:
		bounds[0,1] = r_mid
		bounds[1,1] = m_mid
		bounds[2,0] = s_mid
	elif best_fit == 3:
		bounds[0,0] = r_mid
		bounds[1,1] = m_mid
		bounds[2,0] = s_mid
	elif best_fit == 4:
		bounds[0,1] = r_mid
		bounds[1,0] = m_mid
		bounds[2,0] = s_mid
	elif best_fit == 5:
		bounds[0,1] = r_mid
		bounds[1,0] = m_mid
		bounds[2,1] = s_mid
	elif best_fit == 6:
		bounds[0,0] = r_mid
		bounds[1,0] = m_mid
		bounds[2,1] = s_mid
	elif best_fit == 7:
		bounds[0,0] = r_mid
		bounds[1,0] = m_mid
		bounds[2,0] = s_mid
	else:
		bounds[0,1] = test_points[len(test_points)-1,0]
		bounds[0,0] = test_points[0,0]
		bounds[1,1] = test_points[len(test_points)-1,1]
		bounds[1,0] = test_points[0,1]
		bounds[2,1] = test_points[len(test_points)-1,2]
		bounds[2,0] = test_points[0,2]
	return bounds
